document.addEventListener('DOMContentLoaded', () => {

    if (document.querySelector('#select-dish').hasChildNodes()) {
        document.querySelector('#place-order').style.display = "block";
        sum_shop_cart();
    }

    document.querySelectorAll('.el-close').forEach(cross => {
        cross.onclick = function() {
            delete_element(cross.parentElement);
        }
    });


    document.querySelector('#place-order').onclick = function() {
        const request = new XMLHttpRequest();
        request.open('POST', '/place_order');

        request.onload = () => {
            window.location.href = 'orders'
        };

        const data = new FormData();
        let data_id = {"id": []}
        document.querySelectorAll('.el-id').forEach(dish => {
            const index = data_id['id'].length;
            data_id['id'][index] = dish.innerHTML;
        })
        data.append('id', JSON.stringify(data_id));
        
        request.send(data);
    };
    
    var list_additions = [];
    document.querySelectorAll('.dishes').forEach(menu => {
        menu.onclick = function() {
            const table = menu.parentElement.querySelector('.table');
            
            if (table.style.display == 'inline') {
                table.style.display = 'none';
            }
            else {
                table.style.display = 'inline';
            }
            
            if (menu.parentElement.querySelector('.toppings')) {
                table.classList.toggle('selection');
            }

            table.querySelectorAll('.add').forEach(extra => {
                extra.nextElementSibling.style.display = 'none';
                list_additions.push(extra.parentElement);
            });

            table.querySelectorAll('span').forEach(toggle => {
                toggle.onclick = function() {
                    const switch_size = toggle.parentElement;
                    const dish = switch_size.parentElement;
                    const large_size = dish.querySelector('.lar');
                    if (large_size) {
                        dish.querySelector('.large').style.display = 'none';
                        dish.querySelector('.small').style.display = 'inline';
                        dish.querySelector('.size').innerHTML = 'Small';
                    }
                    else {
                        dish.querySelector('.small').style.display = 'none';
                        dish.querySelector('.large').style.display = 'inline';
                        dish.querySelector('.size').innerHTML = 'Large';
                    }
                    switch_size.classList.toggle('lar');
                };
            });
        };
    });
    var data_toppings = {'data': []};
    var data_additions = {'data': []};
    var num_top = -1;

    document.querySelectorAll('.into-shop-cart').forEach(plus => {
        plus.onclick = function() {
            plus.style.color = "green";
            plus.innerHTML = 'v';
            document.querySelector('#place-order').style.display = "block";
            const user = document.querySelector('.user').innerHTML;
            const dish = plus.parentElement;
            const name = dish.firstElementChild.innerHTML;
            const menu = dish.parentElement.previousElementSibling.innerHTML;
            let size;
            const large_size = dish.querySelector('.lar');
            const no_size = dish.querySelector('.no-size');
            if (large_size) {size = 'L';}
            else if (no_size) {size = '';}
            else {size = 'S';}

            if (name == "1 topping" || name == "1 item") {
                num_top = 1;
                select_toppings(num_top, dish, user, name, menu, size);
            }
            else if (name == "2 toppings" || name == "2 items") {
                num_top = 2;
                select_toppings(num_top, dish, user, name, menu, size);
            }
            else if (name == "3 toppings" || name == "3 items") {
                num_top = 3;
                select_toppings(num_top, dish, user, name, menu, size);
            }

            if (menu === "Subs") {
                num_top = 0;
                const modal = document.querySelector('#selectExtras');
                modal.style.display = "block";
                list_additions.forEach(extra => {
                    document.querySelector('#content').append(extra);
                    const intocart = extra.querySelector('.into-shop-cart');
                    intocart.style.display = 'inline';
                    intocart.onclick = function() {
                        intocart.style.color = "green";
                        intocart.innerHTML = 'v';            
                        const index = data_additions['data'].length;
                        data_additions['data'][index] = extra.firstElementChild.innerHTML;
                    };
                });
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                        data_additions = {'data': []};
                        shopping_cart(menu, name, size, user);
                        num_top = -1;
                        return false;
                    }
                    if (event.target == document.querySelector('.close')) {
                        modal.style.display = "none";
                        data_additions = {'data': []};
                        shopping_cart(menu, name, size, user);
                        num_top = -1;
                        return false;
                    }            
                    if (event.target == document.querySelector('.cancelbtn')) {
                        modal.style.display = "none";
                        data_additions = {'data': []};
                        shopping_cart(menu, name, size, user);
                        num_top = -1;
                        return false;
                    }
            
                    if (event.target == document.querySelector('.readybtn')) {
                        modal.style.display = "none";
                        shopping_cart(menu, name, size, user);
                        num_top = -1;
                        data_additions = {'data': []};
                        return false;
                    }
                };
            }
           
            if (num_top < 0) {
                shopping_cart(menu, name, size, user);
                data_toppings = {'data': []};
            }
        };
    });


    function select_toppings(number, dish, user, name, menu, size) {
        const toppings = document.querySelector('.toppings').nextElementSibling;
        toppings.style.display = 'inline';
        toppings.parentElement.scrollIntoView();
        toppings.querySelectorAll('.into-shop-cart').forEach(tops => {
            tops.onclick = function() {
                tops.style.color = "green";
                tops.innerHTML = 'v';            
                data_toppings['data'][number-1] = tops.parentElement.firstElementChild.innerHTML;
                number -= 1;
                if (number == 0) {
                    toppings.style.display = 'none';
                    dish.parentElement.parentElement.scrollIntoView();
                    shopping_cart(menu, name, size, user);
                    data_toppings = {'data': []};
                    num_top = -1;
                }
            };
        });
    }


    function shopping_cart(menu, name, size, user) {
        const request = new XMLHttpRequest();
        request.open('POST', '/shopping_cart', true);

        request.onload = () => {
            const cart = JSON.parse(request.responseText);
            add_dish(cart.shop_cart);
        };

        const data = new FormData();
        data.append('menu', menu);
        data.append('name', name);
        data.append('size', size);
        data.append('user', user);
        data.append('toppings', JSON.stringify(data_toppings));
        data.append('additions', JSON.stringify(data_additions));

        request.send(data);
        
        return false;
    }


    const cart_template = Handlebars.compile(document.querySelector('#cart_template').innerHTML);    

    function add_dish(data) {
        const dish = cart_template({
            'id': data.id,
            'menu': data.menu,
            'name': data.name,
            'size': data.size,
            'price': data.price,
        });

        document.querySelector('#select-dish').innerHTML += dish;
        
        let extra = document.querySelector('.extra');
        if (data.add1) {
            li = document.createElement('li');
            li.innerHTML = data.add1.name;
            if (data.add1.price) {
                span = document.createElement('span');
                span.classList.add('el-price');
                span.innerHTML = data.add1.price;    
                li.append(span);
            }
            extra.append(li);
        }
        if (data.add2) {
            li = document.createElement('li');
            li.innerHTML = data.add2.name;
            if (data.add2.price) {
                span = document.createElement('span');
                span.classList.add('el-price');
                span.innerHTML = data.add2.price;
                li.append(span);    
            }
            extra.append(li);
        }
        if (data.add3) {
            li = document.createElement('li');
            li.innerHTML = data.add3.name;
            if (data.add3.price) {
                span = document.createElement('span');
                span.classList.add('el-price');
                span.innerHTML = data.add3.price;
                li.append(span);    
            }
            extra.append(li);
        }
        
        extra.classList.remove('extra');    

        document.querySelectorAll('.el-close').forEach(cross => {
            cross.onclick = function() {
                delete_element(cross.parentElement);
            }
        });
    
        sum_shop_cart();
    }


    function delete_element(dish) {        
        const request = new XMLHttpRequest();
        request.open('POST', '/delete_dish', true);

        request.onload = () => {
            const result = JSON.parse(request.responseText);
            if (result.success == 'true') {
                dish.remove();
            }
            sum_shop_cart();
        };

        const data = new FormData();
        data.append('id', dish.querySelector('.el-id').innerHTML);
        
        request.send(data);
        
        return false;

    }

    function sum_shop_cart() {
        let total_sum = 0;
        document.querySelectorAll('.el-price').forEach(price => {
            if (price.innerHTML) {
                total_sum += parseFloat(price.innerHTML);
            }
        });
        document.querySelector('#sum-shop-cart').innerHTML = total_sum;

    }

});