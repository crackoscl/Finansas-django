document.addEventListener(
  "DOMContentLoaded",


  function () {
    document
      .getElementById("id_tipo")
      .addEventListener("change", function () {
        fetch(
          "/finansas/get-categories/?" +
            new URLSearchParams({
              id: this.value,
            }).toString()
        )
          .then((res) => res.json())
          .then(function (data) {    
            const options = data.map((item) => {
              return `<option value=${item.id}>${item.name}</option>`});
            options.unshift('<option value="">---------</option>')
            document.getElementById("id_category").innerHTML = options
          });
      });
  },


  false
);
