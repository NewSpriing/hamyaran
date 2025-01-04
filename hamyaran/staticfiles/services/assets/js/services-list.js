/* const search = () => {
 const searchbox = document.getElementById("search-item").value;
 const serviceitems = document.getElementById("services-list")
 const services = document.querySelectorAll("service")
 const sname = serviceitems.getElementsByTagName("h3")

  for (var i = 0; i < sname.length; i++) {
    let match = services[i].getElementsByTagName("h3")[0];

    if (match) {
      let textvalue = match.textContent || match.innerHTML

      if (textvalue.indexOf(searchbox) > -1) {
        services[i].style.display = "";
      } else {
        services[i].style.display = "none"; 
      }
    }
  }
} */
const search = () => {
  const searchbox = document.getElementById("search-item").value.toLowerCase(); // Case-insensitive search
  const serviceItems = document.getElementById("services-list");
  const services = serviceItems.getElementsByClassName("service"); // Assuming services have class "service"

  for (let i = 0; i < services.length; i++) {
    const match = services[i].getElementsByTagName("h3")[0];

    if (match) {
      const textValue = match.textContent || match.innerHTML;

      // Case-insensitive comparison
      if (textValue.toLowerCase().indexOf(searchbox) > -1) {
        services[i].style.display = ""; // Show the item
      } else {
        services[i].style.display = "none"; // Hide the item
      }
    }
  }
};
