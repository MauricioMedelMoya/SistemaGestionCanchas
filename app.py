from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reservas_canchas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta-ejemplo"

db = SQLAlchemy(app)

ESTADOS_RESERVA = ["pendiente", "confirmada", "cancelada"]
TIPOS_DEPORTE = ["Futbol", "Padel", "Baby futbol", "Multicancha"]


class Cancha(db.Model):
    __tablename__ = "canchas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    tipo_deporte = db.Column(db.String(80), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    precio_por_hora = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    reservas = db.relationship("Reserva", backref="cancha", lazy=True)

    @property
    def precio_hora_calculado(self):
        """Calcula el precio por hora basado en el tipo de deporte"""
        if self.tipo_deporte.lower() == "futbol":
            return Decimal('22000.00')
        else:
            return Decimal('15000.00')

    def __repr__(self):
        return f"<Cancha {self.nombre}>"


class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(120), nullable=False)
    correo_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(30), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    horas_arriendadas = db.Column(db.Integer, nullable=False, default=1)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    observaciones = db.Column(db.String(250), nullable=True)
    cancha_id = db.Column(db.Integer, db.ForeignKey("canchas.id"), nullable=False)

    @property
    def hora_fin(self):
        """Calcula la hora de fin de la reserva"""
        from datetime import datetime, timedelta
        hora_inicio = datetime.strptime(self.hora, '%H:%M').time()
        hora_fin = datetime.combine(self.fecha, hora_inicio) + timedelta(hours=self.horas_arriendadas)
        return hora_fin.time()

    def __repr__(self):
        return f"<Reserva {self.nombre_cliente} - {self.fecha} {self.hora} ({self.horas_arriendadas}h)>"


def obtener_datos_cancha():
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "tipo_deporte": request.form.get("tipo_deporte", "").strip(),
        "ubicacion": request.form.get("ubicacion", "").strip(),
        "disponible": request.form.get("disponible", "1"),
    }


def obtener_datos_reserva():
    return {
        "nombre_cliente": request.form.get("nombre_cliente", "").strip(),
        "correo_cliente": request.form.get("correo_cliente", "").strip(),
        "telefono_cliente": request.form.get("telefono_cliente", "").strip(),
        "fecha": request.form.get("fecha", "").strip(),
        "hora": request.form.get("hora", "").strip(),
        "horas_arriendadas": request.form.get("horas_arriendadas", "1").strip(),
        "estado": request.form.get("estado", "").strip(),
        "observaciones": request.form.get("observaciones", "").strip(),
        "cancha_id": request.form.get("cancha_id", "").strip(),
    }


def validar_decimal(valor):
    try:
        numero = Decimal(valor)
        if numero < 0:
            raise ValueError
        return numero
    except (InvalidOperation, ValueError):
        return None


def validar_fecha(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


def validar_hora(valor):
    try:
        return datetime.strptime(valor, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None


def buscar_reserva_ocupada(cancha_id, fecha, hora, reserva_id=None):
    consulta = Reserva.query.filter(
        Reserva.cancha_id == cancha_id,
        Reserva.fecha == fecha,
        Reserva.hora == hora,
        Reserva.estado != "cancelada",
    )

    if reserva_id:
        consulta = consulta.filter(Reserva.id != reserva_id)

    return consulta.first()


def obtener_disponibilidad(fecha_raw, hora_raw):
    fecha = validar_fecha(fecha_raw) if fecha_raw else None
    hora = validar_hora(hora_raw) if hora_raw else None

    if not fecha or not hora:
        return fecha, hora, [], []

    reservas_ocupadas = Reserva.query.filter(
        Reserva.fecha == fecha,
        Reserva.hora == hora,
        Reserva.estado != "cancelada",
    ).all()
    canchas_ocupadas_ids = {reserva.cancha_id for reserva in reservas_ocupadas}

    disponibles = (
        Cancha.query.filter(Cancha.disponible.is_(True))
        .order_by(Cancha.nombre.asc())
        .all()
    )
    canchas_disponibles = [
        cancha for cancha in disponibles if cancha.id not in canchas_ocupadas_ids
    ]

    return fecha, hora, reservas_ocupadas, canchas_disponibles


with app.app_context():
    db.create_all()

    # Poblar canchas de ejemplo si no existen
    if Cancha.query.count() == 0:
        canchas_ejemplo = [
            Cancha(nombre="Cancha Fútbol 1", tipo_deporte="Futbol", ubicacion="Estadio Central", precio_por_hora=Decimal('22000.00'), disponible=True),
            Cancha(nombre="Cancha Fútbol 2", tipo_deporte="Futbol", ubicacion="Estadio Norte", precio_por_hora=Decimal('22000.00'), disponible=True),
            Cancha(nombre="Cancha Padel 1", tipo_deporte="Padel", ubicacion="Club Deportivo", precio_por_hora=Decimal('15000.00'), disponible=True),
            Cancha(nombre="Cancha Padel 2", tipo_deporte="Padel", ubicacion="Club Deportivo", precio_por_hora=Decimal('15000.00'), disponible=True),
            Cancha(nombre="Cancha Baby Fútbol", tipo_deporte="Baby futbol", ubicacion="Polideportivo Sur", precio_por_hora=Decimal('15000.00'), disponible=True),
            Cancha(nombre="Multicancha", tipo_deporte="Multicancha", ubicacion="Centro Recreativo", precio_por_hora=Decimal('15000.00'), disponible=True),
        ]
        for cancha in canchas_ejemplo:
            db.session.add(cancha)
        db.session.commit()


@app.route("/")
def index():
    total_canchas = Cancha.query.count()
    total_reservas = Reserva.query.count()
    reservas_pendientes = Reserva.query.filter_by(estado="pendiente").count()
    return render_template(
        "index.html",
        total_canchas=total_canchas,
        total_reservas=total_reservas,
        reservas_pendientes=reservas_pendientes,
    )


@app.route("/canchas")
def listar_canchas():
    canchas = Cancha.query.order_by(Cancha.id.desc()).all()
    return render_template("canchas/lista.html", canchas=canchas)


@app.route("/canchas/nueva", methods=["GET", "POST"])
def crear_cancha():
    form_data = obtener_datos_cancha() if request.method == "POST" else None

    if request.method == "POST":
        nombre = form_data["nombre"]
        tipo_deporte = form_data["tipo_deporte"]
        ubicacion = form_data["ubicacion"]
        disponible = form_data["disponible"] == "1"

        if not nombre or not tipo_deporte or not ubicacion:
            flash("Todos los campos principales de la cancha son obligatorios.", "danger")
            return render_template(
                "canchas/form.html",
                cancha=None,
                form_data=form_data,
                tipos_deporte=TIPOS_DEPORTE,
            )

        cancha = Cancha(
            nombre=nombre,
            tipo_deporte=tipo_deporte,
            ubicacion=ubicacion,
            precio_por_hora=Decimal('0.00'),  # Se calcula automáticamente
            disponible=disponible,
        )
        db.session.add(cancha)
        db.session.commit()

        flash("Cancha creada correctamente.", "success")
        return redirect(url_for("listar_canchas"))

    return render_template(
        "canchas/form.html",
        cancha=None,
        form_data=form_data,
        tipos_deporte=TIPOS_DEPORTE,
    )


@app.route("/canchas/editar/<int:id>", methods=["GET", "POST"])
def editar_cancha(id):
    cancha = Cancha.query.get_or_404(id)
    form_data = obtener_datos_cancha() if request.method == "POST" else None

    if request.method == "POST":
        nombre = form_data["nombre"]
        tipo_deporte = form_data["tipo_deporte"]
        ubicacion = form_data["ubicacion"]
        disponible = form_data["disponible"] == "1"

        if not nombre or not tipo_deporte or not ubicacion:
            flash("Todos los campos principales de la cancha son obligatorios.", "danger")
            return render_template(
                "canchas/form.html",
                cancha=cancha,
                form_data=form_data,
                tipos_deporte=TIPOS_DEPORTE,
            )

        cancha.nombre = nombre
        cancha.tipo_deporte = tipo_deporte
        cancha.ubicacion = ubicacion
        cancha.disponible = disponible

        db.session.commit()
        flash("Cancha actualizada correctamente.", "success")
        return redirect(url_for("listar_canchas"))

    return render_template(
        "canchas/form.html",
        cancha=cancha,
        form_data=form_data,
        tipos_deporte=TIPOS_DEPORTE,
    )


@app.route("/canchas/eliminar/<int:id>", methods=["POST"])
def eliminar_cancha(id):
    cancha = Cancha.query.get_or_404(id)

    if cancha.reservas:
        flash("No se puede eliminar una cancha que ya tiene reservas asociadas.", "danger")
        return redirect(url_for("listar_canchas"))

    db.session.delete(cancha)
    db.session.commit()

    flash("Cancha eliminada correctamente.", "warning")
    return redirect(url_for("listar_canchas"))


@app.route("/reservas")
def listar_reservas():
    fecha_raw = request.args.get("fecha", "").strip()
    hora_raw = request.args.get("hora", "").strip()
    fecha, hora, reservas_ocupadas, canchas_disponibles = obtener_disponibilidad(
        fecha_raw, hora_raw
    )

    reservas = Reserva.query.order_by(Reserva.fecha.desc(), Reserva.hora.desc()).all()
    return render_template(
        "reservas/lista.html",
        reservas=reservas,
        fecha_busqueda=fecha_raw,
        hora_busqueda=hora_raw,
        fecha=fecha,
        hora=hora,
        reservas_ocupadas=reservas_ocupadas,
        canchas_disponibles=canchas_disponibles,
    )


@app.route("/reservas/nueva", methods=["GET", "POST"])
def crear_reserva():
    canchas = Cancha.query.order_by(Cancha.nombre.asc()).all()
    form_data = obtener_datos_reserva() if request.method == "POST" else None

    if request.method == "POST":
        nombre_cliente = form_data["nombre_cliente"]
        correo_cliente = form_data["correo_cliente"]
        telefono_cliente = form_data["telefono_cliente"]
        fecha = validar_fecha(form_data["fecha"])
        hora = validar_hora(form_data["hora"])
        horas_arriendadas = int(form_data["horas_arriendadas"]) if form_data["horas_arriendadas"].isdigit() else 1
        estado = form_data["estado"]
        observaciones = form_data["observaciones"]

        try:
            cancha_id = int(form_data["cancha_id"])
        except ValueError:
            cancha_id = None

        cancha = Cancha.query.get(cancha_id) if cancha_id else None

        if not canchas:
            flash("Debes crear al menos una cancha antes de registrar reservas.", "danger")
            return redirect(url_for("listar_canchas"))

        if not nombre_cliente or not correo_cliente or not telefono_cliente:
            flash("Los datos del cliente son obligatorios.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not fecha or not hora:
            flash("La fecha y la hora deben tener un formato valido.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if estado not in ESTADOS_RESERVA:
            flash("El estado seleccionado no es valido.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not cancha:
            flash("Debes seleccionar una cancha valida.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not cancha.disponible and estado != "cancelada":
            flash("La cancha seleccionada no esta disponible para nuevas reservas.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        # Validar horario ocupado
        if estado != "cancelada" and buscar_reserva_ocupada(cancha.id, fecha, hora):
            flash("Ya existe una reserva activa para esa cancha en la misma fecha y hora.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=None,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        reserva = Reserva(
            nombre_cliente=nombre_cliente,
            correo_cliente=correo_cliente,
            telefono_cliente=telefono_cliente,
            fecha=fecha,
            hora=hora,
            horas_arriendadas=horas_arriendadas,
            precio_total=cancha.precio_hora_calculado * horas_arriendadas,
            estado=estado,
            observaciones=observaciones,
            cancha_id=cancha.id,
        )
        db.session.add(reserva)
        db.session.commit()

        flash("Reserva creada correctamente.", "success")
        return redirect(url_for("listar_reservas"))

    return render_template(
        "reservas/form.html",
        reserva=None,
        form_data=form_data,
        canchas=canchas,
        estados=ESTADOS_RESERVA,
    )


@app.route("/reservas/editar/<int:id>", methods=["GET", "POST"])
def editar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    canchas = Cancha.query.order_by(Cancha.nombre.asc()).all()
    form_data = obtener_datos_reserva() if request.method == "POST" else None

    if request.method == "POST":
        nombre_cliente = form_data["nombre_cliente"]
        correo_cliente = form_data["correo_cliente"]
        telefono_cliente = form_data["telefono_cliente"]
        fecha = validar_fecha(form_data["fecha"])
        hora = validar_hora(form_data["hora"])
        horas_arriendadas = int(form_data["horas_arriendadas"]) if form_data["horas_arriendadas"].isdigit() else 1
        estado = form_data["estado"]
        observaciones = form_data["observaciones"]

        try:
            cancha_id = int(form_data["cancha_id"])
        except ValueError:
            cancha_id = None

        cancha = Cancha.query.get(cancha_id) if cancha_id else None

        if not nombre_cliente or not correo_cliente or not telefono_cliente:
            flash("Los datos del cliente son obligatorios.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not fecha or not hora:
            flash("La fecha y la hora deben tener un formato valido.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if estado not in ESTADOS_RESERVA:
            flash("El estado seleccionado no es valido.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not cancha:
            flash("Debes seleccionar una cancha valida.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if not cancha.disponible and estado != "cancelada":
            flash("La cancha seleccionada no esta disponible para nuevas reservas.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        if estado != "cancelada" and buscar_reserva_ocupada(cancha.id, fecha, hora, reserva.id):
            flash("Ya existe una reserva activa para esa cancha en la misma fecha y hora.", "danger")
            return render_template(
                "reservas/form.html",
                reserva=reserva,
                form_data=form_data,
                canchas=canchas,
                estados=ESTADOS_RESERVA,
            )

        reserva.nombre_cliente = nombre_cliente
        reserva.correo_cliente = correo_cliente
        reserva.telefono_cliente = telefono_cliente
        reserva.fecha = fecha
        reserva.hora = hora
        reserva.horas_arriendadas = horas_arriendadas
        reserva.precio_total = cancha.precio_hora_calculado * horas_arriendadas
        reserva.estado = estado
        reserva.observaciones = observaciones
        reserva.cancha_id = cancha.id

        db.session.commit()
        flash("Reserva actualizada correctamente.", "success")
        return redirect(url_for("listar_reservas"))

    return render_template(
        "reservas/form.html",
        reserva=reserva,
        form_data=form_data,
        canchas=canchas,
        estados=ESTADOS_RESERVA,
    )


@app.route("/reservas/eliminar/<int:id>", methods=["POST"])
def eliminar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()

    flash("Reserva eliminada correctamente.", "warning")
    return redirect(url_for("listar_reservas"))


@app.route("/calendario")
def calendario():
    fecha_raw = request.args.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    fecha = validar_fecha(fecha_raw)

    if not fecha:
        fecha = datetime.now().date()
        fecha_raw = fecha.strftime("%Y-%m-%d")

    canchas = Cancha.query.filter_by(disponible=True).order_by(Cancha.nombre.asc()).all()

    # Obtener reservas para esa fecha
    reservas_dia = Reserva.query.filter(
        Reserva.fecha == fecha,
        Reserva.estado != "cancelada"
    ).order_by(Reserva.hora.asc()).all()

    # Agrupar reservas por cancha
    reservas_por_cancha = {}
    for reserva in reservas_dia:
        if reserva.cancha_id not in reservas_por_cancha:
            reservas_por_cancha[reserva.cancha_id] = []
        reservas_por_cancha[reserva.cancha_id].append(reserva)

    return render_template(
        "calendario.html",
        fecha=fecha,
        fecha_raw=fecha_raw,
        canchas=canchas,
        reservas_por_cancha=reservas_por_cancha,
    )


if __name__ == "__main__":
    app.run(debug=True)
