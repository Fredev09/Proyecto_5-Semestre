document.addEventListener("DOMContentLoaded", function () {

  // Animaciones
  AOS.init({
    duration: 1000,
    once: true
  });

  // ======================
  // MAPA
  // ======================
  const map = L.map("map").setView([4.5709, -74.2973], 6);

  const iconoSede = L.divIcon({
    className: "",
    html: `
      <div style="
        position: relative;
        width: 18px;
        height: 18px;
        background: white;
        border-radius: 50%;
        border: 3px solid #C62828;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
      ">
        <div style="
          position: absolute;
          top: 50%;
          left: 50%;
          width: 40px;
          height: 40px;
          background: rgba(198, 40, 40, 0.3);
          border-radius: 50%;
          transform: translate(-50%, -50%);
          animation: pulse 1.5s infinite;
        "></div>
      </div>
    `,
    iconSize: [20, 20]
  });

  // Marcador principal
  L.marker([8.74798, -75.88143], { icon: iconoSede })
    .addTo(map)
    .bindPopup("<strong>Montería</strong><br>Sede de la empresa")
    .openPopup();

  // Cargar mapa Colombia
  fetch("/static/js/colombia.geojson")
    .then(res => res.json())
    .then(data => {

      const colombiaLayer = L.geoJSON(data, {
        style: {
          color: "#8B0000",
          weight: 2,
          fillColor: "#C62828",
          fillOpacity: 0.6
        },

        onEachFeature: function (feature, layer) {
          const nombre = feature.properties.NOMBRE_DPT || "Departamento";

          layer.bindPopup(`<strong>${nombre}</strong>`);

          layer.on({
            mouseover: function () {
              layer.setStyle({
                fillColor: "#FF5252",
                fillOpacity: 0.9
              });
            },
            mouseout: function () {
              layer.setStyle({
                fillColor: "#C62828",
                fillOpacity: 0.6
              });
            }
          });
        }

      }).addTo(map);

      map.fitBounds(colombiaLayer.getBounds());
    });

  map.setMaxBounds([
    [-4.5, -81.7],
    [13.5, -66.8]
  ]);

  // ======================
  // ZONAS (ARREGLADO)
  // ======================
  const zonasTrabajo = [
    {
      nombre: "La Unión (Sucre)",
      coords: [8.8606, -75.2833],
      descripcion: "Proyecto en el municipio de La Unión, Sucre.",
      scroll: false
    },
    {
      nombre: "Abriaquí (Antioquia)",
      coords: [6.6278, -76.0647],
      descripcion: "Proyecto en Abriaquí, Antioquia.",
      scroll: false
    },
    {
      nombre: "Montelíbano",
      id: "montelibano",
      coords: [7.9792, -75.4200],
      descripcion: "Proyecto en Montelíbano, Córdoba.",
      scroll: true
    },
    {
      nombre: "Majagual",
      id: "majagual",
      coords: [8.5361, -74.6314],
      descripcion: "Proyecto en Majagual, Sucre.",
      scroll: true
    },
    {
      nombre: "Moñitos",
      id: "monitos",
      coords: [9.2456, -76.1361],
      descripcion: "Proyecto en Moñitos, Córdoba.",
      scroll: true
    }
  ];

  zonasTrabajo.forEach(zona => {

    const marker = L.marker(zona.coords).addTo(map);

    if (zona.scroll) {
      marker.bindPopup(`
        <strong>${zona.nombre}</strong><br>
        ${zona.descripcion}<br><br>
        <button class="boton-mapa" onclick="irAProyecto('${zona.id}')">
          Ver proyecto
        </button>
      `);

      marker.on("click", function () {
        irAProyecto(zona.id);
      });

    } else {
      marker.bindPopup(`
        <strong>${zona.nombre}</strong><br>
        ${zona.descripcion}
      `);
    }

  });

  // ======================
  // FUNCIÓN SCROLL (ARREGLADA)
  // ======================
  window.irAProyecto = function(id) {
    const elemento = document.getElementById(id);

    if (elemento) {
      elemento.scrollIntoView({ behavior: "smooth" });

      elemento.style.boxShadow = "0 0 25px rgba(198,40,40,0.7)";
      setTimeout(() => {
        elemento.style.boxShadow = "";
      }, 1500);

    } else {
      console.log("No se encontró:", id);
    }
  };

  // ======================
  // FORMULARIO
  // ======================
    const form = document.querySelector(".contact-form");
    const popup = document.getElementById("custom-popup");
    const popupBtn = document.getElementById("popup-btn");

          if (form) {

          form.addEventListener("submit", function(e) {

          e.preventDefault();

          const nombre = form.querySelector('[name="nombre"]').value.trim();
          const telefono = form.querySelector('[name="telefono"]').value.trim();
          const correo = form.querySelector('[name="correo"]').value.trim();
          const servicio = form.querySelector('[name="servicio"]').value.trim();
          const mensaje = form.querySelector('[name="mensaje"]').value.trim();

          if (!nombre || !telefono || !correo || !servicio || !mensaje) {

            alert("Por favor completa todos los campos.");

            return;
          }
          popup.classList.add("active");
        });
      }
        popupBtn.addEventListener("click", () => {
        popup.classList.remove("active");
        setTimeout(() => {
          form.submit();
        }, 500);

});

  // ======================
  // CARRUSEL SERVICIOS
  // ======================
  const track = document.querySelector(".slider-track");
  const slides = document.querySelectorAll(".service");
  const nextBtn = document.querySelector(".next");
  const prevBtn = document.querySelector(".prev");

  let index = 0;

  function updateSlider() {
    track.style.transform = `translateX(-${index * 100}%)`;
  }

  if (track && slides.length > 0 && nextBtn && prevBtn) {
    nextBtn.addEventListener("click", function () {
      index++;

      if (index >= slides.length) {
        index = 0;
      }

      updateSlider();
    });

    prevBtn.addEventListener("click", function () {
      index--;

      if (index < 0) {
        index = slides.length - 1;
      }

      updateSlider();
    });
  }

  

});

let servicioActual = 0;

function mostrarSlideServicio(index) {
  const slides = document.querySelectorAll(".servicio-slide");
  const dots = document.querySelectorAll(".servicio-dots .dot");

  if (!slides.length) return;

  slides.forEach(slide => slide.classList.remove("active"));
  dots.forEach(dot => dot.classList.remove("active"));

  slides[index].classList.add("active");
  dots[index].classList.add("active");
}

function cambiarServicio(direccion) {
  const slides = document.querySelectorAll(".servicio-slide");

  servicioActual += direccion;

  if (servicioActual >= slides.length) {
    servicioActual = 0;
  }

  if (servicioActual < 0) {
    servicioActual = slides.length - 1;
  }

  mostrarSlideServicio(servicioActual);
}

function irServicio(index) {
  servicioActual = index;
  mostrarSlideServicio(servicioActual);
}

// ======================
// MODAL CLIENTES CONSTRUCTORA
// ======================

document.addEventListener("DOMContentLoaded", () => {

    const clientModal = document.getElementById("client-modal");
    const openClientModal = document.getElementById("open-client-modal");
    const closeClientModal = document.getElementById("close-client-modal");

    // ABRIR
    if(openClientModal){
        openClientModal.addEventListener("click", () => {
            clientModal.classList.add("active");

        });

    }

    // CERRAR X

    if(closeClientModal){
        closeClientModal.addEventListener("click", () => {
            clientModal.classList.remove("active");
        });

    }

    // CERRAR AFUERA

    if(clientModal){
        clientModal.addEventListener("click", (e) => {
            if(e.target === clientModal){
                clientModal.classList.remove("active");

            }

        });

    }

});

let proyectoEliminar = null;

function abrirPopupEliminar(id){
    proyectoEliminar = id;
    document.getElementById('popupEliminar')
        .classList.add('active');
}

function cerrarPopupEliminar(){
    document.getElementById('popupEliminar')
        .classList.remove('active');
}

document.getElementById('btnConfirmarEliminar')
.addEventListener('click', function(){
    window.location.href =
        "/eliminar_proyecto/" + proyectoEliminar;
});

const modal = document.getElementById('client-modal');
const openBtn = document.getElementById('open-client-modal');
const closeBtn = document.getElementById('close-client-modal');

openBtn.addEventListener('click', () => {
    modal.classList.add('active');
});

closeBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});

window.addEventListener('click', (e) => {
    if(e.target === modal){
        modal.classList.remove('active');
    }
});

const inmuebleSelect = document.getElementById("inmuebleSelect");
const valorVenta = document.getElementById("valorVenta");
const slider = document.getElementById("anticipoSlider");

const porcentajeTexto = document.getElementById("porcentajeTexto");
const valorAnticipo = document.getElementById("valorAnticipo");
const saldoPendiente = document.getElementById("saldoPendiente");

const anticipoInput = document.getElementById("anticipoInput");
const saldoInput = document.getElementById("saldoInput");

function formatoMoneda(valor) {
    return new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        minimumFractionDigits: 0
    }).format(valor);
}

function calcularAnticipo() {
    const precio = Number(valorVenta.value || 0);
    const porcentaje = Number(slider.value || 0);

    const anticipo = precio * porcentaje / 100;
    const saldo = precio - anticipo;

    porcentajeTexto.textContent = porcentaje + "%";
    valorAnticipo.textContent = formatoMoneda(anticipo);
    saldoPendiente.textContent = formatoMoneda(saldo);

    anticipoInput.value = anticipo;
    saldoInput.value = saldo;
}

inmuebleSelect.addEventListener("change", function () {
    const opcion = this.options[this.selectedIndex];
    const precio = opcion.dataset.precio || 0;

    valorVenta.value = precio;
    slider.value = 0;

    calcularAnticipo();
});

slider.addEventListener("input", calcularAnticipo);

const ingresosData = {{ ingresos_grafico | tojson }};
    const estados = {{ estado_inmuebles | tojson }};

    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    const ingresosPorMes = Array(12).fill(0);

    ingresosData.forEach(item => {
        ingresosPorMes[item.mes - 1] = item.ingresos;
    });

    new Chart(document.getElementById('finanzasChart'), {
        type: 'bar',
        data: {
            labels: meses,
            datasets: [
                {
                    label: 'Ingresos',
                    data: ingresosPorMes,
                    backgroundColor: '#981313',
                    borderRadius: 8
                }
            ]
        }
    });

    new Chart(document.getElementById('inmueblesChart'), {
        type: 'pie',
        data: {
            labels: ['Disponibles', 'Reservados', 'Vendidos'],
            datasets: [{
                data: [
                    estados.disponibles || 0,
                    estados.reservados || 0,
                    estados.vendidos || 0
                ],
                backgroundColor: ['#1f9d55', '#c58a00', '#981313']
            }]
        }
    });