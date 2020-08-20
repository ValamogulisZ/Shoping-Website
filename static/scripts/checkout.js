var div_order = document.querySelector(".cart"),
  order,
  menu,
  order_input = document.getElementById("checkout_json");


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

function displayOrder() {
  div_order.innerHTML = "";
  if (order.length === 0) {
    div_order.innerHTML = "There is nothing in your order!";
  } else {
    var total_price = 0;
    setCookie("order", JSON.stringify(order), 365);
    order_input.value = JSON.stringify(order);
    order.forEach(function(product) {
      var menu_index = checkProductIndex(product.id, menu);
      var product_info = createElement("div", [{
        attr_name: "class",
        attr_value: "columns product"
      }], "");
      var div_img = createElement("div", [{
        attr_name: "class",
        attr_value: "column is-2 img"
      }], "");
      div_img.appendChild(createElement("img", [{
        attr_name: "src",
        attr_value: menu[menu_index].imageURL
      }, {
        attr_name: "alt",
        attr_value: "Temporary no pictures"
      }], ""));
      product_info.appendChild(div_img);
      var info = createElement("div", [{
        attr_name: "class",
        attr_value: "column is-8 info"
      }], "");
      info.appendChild(createElement("p", [{
        attr_name: "class",
        attr_value: "name"
      }], menu[menu_index].name));
      info.appendChild(createElement("p", [{
        attr_name: "class",
        attr_value: "qty"
      }], "$" + menu[menu_index].price + " × " + product.qty));
      product_info.appendChild(info);
      product_info.appendChild(createElement("button", [{
        attr_name: "class",
        attr_value: "button is-danger"
      }, {
        attr_name: "type",
        attr_value: "button"
      }, {
        attr_name: "onclick",
        attr_value: "removeFromCart(" + product.id + ")"
      }], "Remove"));
      div_order.appendChild(product_info);
      total_price += parseFloat(menu[menu_index].price) * product.qty;
    });
    div_order.appendChild(createElement("h3", [{
      attr_name: "style",
      attr_value: "text-align: right;"
    }], "Total: $" + total_price));
  }
}

function removeFromCart(product_id) {
  var order_index = checkProductIndex(product_id, order);
  if(order_index !== -1) {
    order.splice(order_index, 1);
    displayOrder();
    order_input.value = JSON.stringify(order);
  }
}

window.onload = function() {
  setTimeout(function(){
    order = JSON.parse(getCookie("order"));
    menu = JSON.parse(getCookie("menu"));
    displayOrder();

  }, 750);
};
