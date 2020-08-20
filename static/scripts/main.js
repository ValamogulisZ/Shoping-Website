var api = "",
  div_menu = document.querySelector(".menu-product"),
  div_order = document.querySelector(".modal-body"),
  modal_switch = document.getElementById("modal_cart"),
  menu,
  order = [];

function createElement(element_type, attr, innerhtml) {
  var element = document.createElement(element_type);
  if (attr.length > 0) {
    for (var i = 0; i < attr.length; i++) {
      element.setAttribute(attr[i].attr_name, attr[i].attr_value);
    }
  }
  if (innerhtml !== "") {
    element.innerHTML = innerhtml;
  }
  return element;
}

function displayOrder() {
  div_order.innerHTML = "";
  if(order.length === 0) {
    div_order.innerHTML = "There is nothing in your order!";
  } else {
    setCookie("order", JSON.stringify(order), 365);
    var total_price = 0;
    order.forEach(function(product) {
      var menu_index = checkProductIndex(product.id, menu);
      var product_info = createElement("div", [{attr_name: "class", attr_value: "columns product"}], "");
      var div_img = createElement("div", [{attr_name: "class", attr_value: "column is-2 img"}], "");
      div_img.appendChild(createElement("img", [{attr_name: "src", attr_value: menu[menu_index].imageURL}, {attr_name: "alt", attr_value: "Temporary no pictures"}], ""));
      product_info.appendChild(div_img);
      var info = createElement("div", [{attr_name: "class", attr_value: "column is-8 info"}], "");
      info.appendChild(createElement("p", [{attr_name: "class", attr_value: "name"}], menu[menu_index].name));
      info.appendChild(createElement("p", [{attr_name: "class", attr_value: "quantity"}], "$" + menu[menu_index].price + " × " + product.qty));
      product_info.appendChild(info);
      product_info.appendChild(createElement("button", [{attr_name: "class",attr_value: "button is-danger"}, {attr_name: "type", attr_value: "button"}, {attr_name: "onclick", attr_value: "removeFromCart(" + product.id + ")"}], "Remove"));
      div_order.appendChild(product_info);
      total_price += parseFloat(menu[menu_index].price) * product.qty;
    });
    div_order.appendChild(createElement("h3", [{attr_name: "style", attr_value: "text-align: right;"}], "Total: $" + total_price));
  }
}

function checkProductIndex(product_id, product_set) {
  var target = -1;
  if (product_set.length !== 0) {
    for (var i = 0; i < product_set.length; i++) {
      if (product_set[i].id == product_id) {
        target = i;
        break;
      }
    }
  }
  return target;
}

function addToCart(product_id) {
  var order_index = checkProductIndex(product_id, order),
    menu_index = checkProductIndex(product_id, menu),
    qty = document.getElementById("f" + product_id);
  if (menu_index !== -1 && parseFloat(qty.value) >= 1) {
    if (order_index === -1) {
      var product = Object.assign({}, menu[menu_index]);
      product.quantity = parseFloat(qty.value);
      order.push({id: product_id, qty: parseFloat(qty.value)});
    } else {
      order[order_index].qty += parseFloat(qty.value);
    }
    qty.value = 1;
    displayOrder();
    modal();
  }
}

function removeFromCart(product_id) {
  var order_index = checkProductIndex(product_id, order);
  if(order_index !== -1) {
    order.splice(order_index, 1);
    displayOrder();
  }
}

function checkOut(elem) {
  elem.classList.add("is-loading");
  elem.disabled = true;
  setTimeout(function(){
    elem.classList.remove("is-loading");
    elem.disabled = false;
    if (order.length !== 0){
      var json_menu = JSON.stringify(menu),
        json_order = JSON.stringify(order);
      setCookie("order", json_order, 365);
      setCookie("menu", json_menu, 365);
      location.href = "/checkout";
    }
  }, 600);
}

function modal(action) {
  if(modal_switch.classList.value.indexOf("is-active") === -1) {
    modal_switch.classList.add("is-active");
  } else {
    modal_switch.classList.remove("is-active");
  }
}

window.onload = function() {
  setTimeout(function(){
    // get goods
    menu = [];
    var img = document.querySelectorAll(".menu-product .product .img img"),
      name = document.querySelectorAll(".menu-product .product .name"),
      tag = document.querySelectorAll(".menu-product .product .prod-tag"),
      inv = document.querySelectorAll(".menu-product .product .prod-inv"),
      price = document.querySelectorAll(".menu-product .product .dollar"),
      pid = document.querySelectorAll(".menu-product .product input");
    for(var i = 0; i < img.length; i++) {
      menu.push({
        id: parseFloat(pid[i].id.substring(1)),
        name: name[i].innerHTML,
        imageURL: img[i].src,
        tag: tag[i].innerHTML,
        inv: inv[i].innerHTML,
        price: parseFloat(price[i].innerHTML)
      });
    }
    var retrOrder = getCookie("order");
    if(retrOrder !== null && retrOrder !== "") {
      order = JSON.parse(retrOrder);
      eraseCookie("menu");
    }
    displayOrder();
  }, 750);



  // set scroll event
  if (window.pageYOffset <= 30) {
    nav_swich = true;
  }
  document.querySelectorAll(".modal-switch").forEach(function(modal_switches) {
    modal_switches.addEventListener("click", function(){
      modal();
    });
  })
  window.addEventListener("scroll", function() {
    scrollCheck(window.pageYOffset);
  });
};
