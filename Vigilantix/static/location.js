// import Cookies from 'js-cookie'

console.log("THis script is woring")

function bttnIS() {
  console.log("Hey this is Me !!")

  const successCallback = (position) => {
    // console.log(position);
    console.log(position.coords.latitude, "This is the latitude ");
    console.log(position.coords.longitude, "This is the longitude ");


    const xhr = new XMLHttpRequest();
    xhr.open('POST', "/getLocation");
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    xhr.onload = () => {
      console.log(xhr.responseText);
    };

    xhr.onerror = () => {
      console.log('Error occurred while making the request');
    };

    xhr.send(JSON.stringify({ latitude: position.coords.latitude, longitude: position.coords.longitude }));
  };

  const errorCallback = (error) => {
    console.log(error);
  };

  navigator.geolocation.getCurrentPosition(successCallback, errorCallback);

}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



