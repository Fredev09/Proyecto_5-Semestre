document.addEventListener("DOMContentLoaded", function () {
// Animaciones
AOS.init({
  duration: 1000,
  once: true
});

// Carrusel
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");

function changeSlide() {
  slides[currentSlide].classList.remove("active");
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add("active");
}

setInterval(changeSlide, 4500);

// Mapa de Colombia
const map = L.map("map").setView([4.5709, -74.2973], 6);

L.marker([4.7110, -74.0721])
  .addTo(map)
  .bindPopup("Bogotá")
  .openPopup();

fetch("/static/colombia.geojson")
  .then(res => res.json())
  .then(data => {
    const colombiaLayer = L.geoJSON(data, {
      style: {
        color: "#8B0000",      // borde rojo oscuro
        weight: 2,
        fillColor: "#C62828",  // rojo principal
        fillOpacity: 0.6
      }
    }).addTo(map);

    map.fitBounds(colombiaLayer.getBounds());
    })
    .catch(error => {
      console.error("Error cargando GeoJSON:", error);
  });

const colombiaBounds = [
  [ -4.5, -81.7 ],
  [ 13.5, -66.8 ]
];

fetch("/static/colombia.geojson")
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

map.setMaxBounds(colombiaBounds);

// Zonas de ejemplo
const zonasTrabajo = [
  {
    ciudad: "Bogotá",
    coords: [4.7110, -74.0721],
    descripcion: "Proyectos residenciales y comerciales."
  },
  {
    ciudad: "Medellín",
    coords: [6.2442, -75.5812],
    descripcion: "Obras de infraestructura urbana."
  },
  {
    ciudad: "Cali",
    coords: [3.4516, -76.5320],
    descripcion: "Adecuaciones civiles y consultoría."
  },
  {
    ciudad: "Barranquilla",
    coords: [10.9685, -74.7813],
    descripcion: "Proyectos de construcción institucional."
  },
  {
    ciudad: "Bucaramanga",
    coords: [7.1193, -73.1227],
    descripcion: "Diseño estructural e interventoría."
  }
];

zonasTrabajo.forEach(zona => {
  L.marker(zona.coords)
    .addTo(map)
    .bindPopup(`
      <strong>${zona.ciudad}</strong><br>
      ${zona.descripcion}
    `);
});

// Formulario provisional
const form = document.querySelector(".contact-form");

form.addEventListener("submit", function(e) {
  e.preventDefault();
  alert("Mensaje enviado correctamente. Más adelante se conectará con la base de datos.");
  form.reset();
});
});