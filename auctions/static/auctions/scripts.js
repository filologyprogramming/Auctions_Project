
// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

// Listen to add_to_wishlist button and block submission
// Wait for all content to be loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get a button
    let add_to_watchlist = document.querySelector("#add_to_watchlist_form");
    // Check if it's on HTML
    if (add_to_watchlist){
        // Block submission
        add_to_watchlist.addEventListener("submit", function(e) {
            e.preventDefault();
    
            // Get ID of listing
            let listing_id = document.querySelector(".listing_id").value;
            
            // Get value of a button - "Add..." or "Remove..."
            let input = document.querySelector("#add_to_watchlist");
            console.log(input);
            
            if (input.value == "Add to watchlist") {
                // Sent listing ID to view
                response = fetch(`/add_to_watchlist/${listing_id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify ({
                        'listing_id': listing_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (input.value == "Add to watchlist") {
                        input.value = "Remove from watchlist"
                    }
                    else {
                        input.value == "Add to watchlist"
                    }
                })
                .catch(error => console.error('Error:', error));
            }
            else {
                response = fetch(`/remove_from_watchlist/${listing_id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify ({
                        'listing_id': listing_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (input.value == "Remove from watchlist") {
                        input.value = "Add to watchlist"
                    }
                    else {
                        input.value == "Remove to watchlist"
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }) 
    }

    // Add a comment code
    // Find add_comment form and block submission
    let add_comment = document.querySelector("#add_comment_form");
    if (add_comment) {
        add_comment.addEventListener("submit", function(f) {
            f.preventDefault();
        
            // Get value of the comment and value of listing ID
            let comment_text = document.querySelector("#comment_form").value;
            let listing_id = document.querySelector(".listing_id").value;

            response = fetch(`/add_comment/${listing_id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify ({
                        'listing_id': listing_id,
                        'comment_text': comment_text
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        let empty_comment = document.querySelector("#empty_comment");
                        empty_comment.style.display = "block";
                        setTimeout (function () 
                            {empty_comment.style.display = "none"}, 2000);
                    }
                    else {
                        console.log(data);
                        // Creates a flag when a comment is added
                        localStorage.setItem("CommentsFlag", ".comment");
                        // Reload the page after comment is added
                        location.reload();    
                    }
                })
                .catch(error => console.error('Error:', error));
            });  
        }
        
        // Once window reloads, scroll to comments section
        
        // Get price form element and block submission
        let price_form = document.querySelector("#place_a_bid_form");
        if (price_form) {
            price_form.addEventListener("submit", function(g) {
                g.preventDefault();
                
                // Get a bid typed by user
                let bid = document.querySelector("#bid");
                if (bid == null) {
                    bid = '';
                }
                else {
                    bid = document.querySelector("#bid").value;
                }
                // Get listing id
                let listing_id = document.querySelector(".listing_id").value;
                
                // Send a bid for further validation
                response = fetch(`/place_a_bid/${listing_id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify ({
                        'listing_id': listing_id,
                        'bid': bid
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    location.reload();
                    
                })
                .catch(error => console.error('Error:', error));
            })
        }
        
        // Watchlist.html
        // Choose all remove_from_watchlist forms
        let remove_from_watchlist = document.querySelectorAll(".remove_from_watchlist");
        // Block submission on each button
        for (let i = 0; i < remove_from_watchlist.length; i++){
            remove_from_watchlist[i].addEventListener("submit", function(e) {
                e.preventDefault();
                
                // Find a child with ID of listing_id from the form which was just clicked/submitted
                let listing_id = e.target.querySelector(".listing_id").value;
                
                // Sent listing ID to view
                let response = fetch(`/remove_from_watchlist/${listing_id}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify ({
                        'listing_id': listing_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    listing = document.querySelector(`#listing_${listing_id}`);
                    listing.remove();
                    location.reload();
                })
                .catch(error => console.error('Error:', error));
            })    
        }
        
        // Categories.html
        // Get the form
        let categories = document.querySelector("#categories_form");
        if (categories) {
            // Get the option user interacts with
            let selected_category = document.querySelector("#selected_category");
            // If user changes item on list
            selected_category.addEventListener("change", function() {
                
                // Deletes all listings - works like a web refresh without refreshing
                // Find the parent in the html
                let parent_element = document.querySelector("#list_of_listings");
                if (parent_element != null) {
                    // Get all children of a parent
                    let children = parent_element.getElementsByTagName("*");
                    for (let i = children.length - 1; i >= 0; i--)
                        // Define children
                    children[i].remove();
                    
                }
                
                // Send chosen category to Django view
                response = fetch(`show_listing_categories?data=${selected_category.value}`, {
                    method: "GET"
                })
                .then(response => response.json())
                .then(data => {
                    // Go over through all listings
                    for (let i = 0; i < data.listings.length; i++) {
                        // Create a structure for each listing
                        // Create a grandparent
                        let list_of_listings = document.querySelector("#list_of_listings");
                        let listing_grandparent = document.createElement("div");
                        list_of_listings.appendChild(listing_grandparent);
                        // Create first and only parent
                        let parent1 = document.createElement("a");
                        listing_grandparent.appendChild(parent1);
                        
                        // Create first child
                        let child1 = document.createElement("div");
                        parent1.appendChild(child1);
                        
                        // Create second child
                        let child2 = document.createElement("div");
                        parent1.appendChild(child2);
                        
                        // Create image tag for 1st child (left side)
                        let image = document.createElement("img");
                        child1.appendChild(image);
                        
                        // Create tags for 2nd child (right side)
                        elo_class = document.createElement("div");
                        lol_class = document.createElement("div");
                        heading4 = document.createElement("h4");
                        heading4v2 = document.createElement("h4");
                        p0 = document.createElement("p");
                        p1 = document.createElement("p");
                        child2.appendChild(elo_class);
                        child2.appendChild(lol_class);
                        elo_class.appendChild(heading4);
                        elo_class.appendChild(heading4v2);
                        lol_class.appendChild(p0);
                        lol_class.appendChild(p1);
                        
                        // Give classes to grandparent (main div)  
                        listing_grandparent.className = "row justify-content-center listing"
                        
                        // Give classes to parent (link)
                        let listing_id = data.listings[i].id;
                        let listing_name = data.listings[i].name;
                        parent1.setAttribute('href', `/${listing_id}/${listing_name}`);
                        parent1.className = "col-12"
                        
                        // Give classes to children
                        child1.className = "col-6 left_side image";
                        child2.className = "col-6 right_side";
                        
                        // Give classes to grandchildren
                        elo_class.className = "elo";
                        lol_class.className = "lol";
                        
                        
                        // Add the source to the picture
                        let image_url = data.listings[i].image;
                        let image_description = data.listings[i].description;
                        image.setAttribute('src', `${image_url}`);
                        image.setAttribute('alt', `${image_description}`);
                        
                        // Set the content of each element
                        heading4.textContent = data.listings[i].name;
                        heading4.setAttribute("class", "listing-name");
                        heading4v2.textContent = "PLN " + data.listings[i].price;
                        heading4v2.setAttribute("class", "listing-price");
                        p0.textContent = data.listings[i].condition;
                        p0.setAttribute("class", "listing-condition");
                        let iso_date = data.listings[i].date;
                        let formatted_date = iso_date.substring(0,10);
                        p1.textContent = formatted_date;
                        
                        p1.setAttribute("class", "listing-date");
                    }
                    // Change the url
                    // history.pushState(null, null, `categories/${selected_category.value}`)
                })
                .catch(error => {
                    console.log("Error", error);
                });
            })
        }
        
        // If link is clicked it gets highlighted as active
        document.querySelectorAll(".nav-link").forEach((link) => {
            if (link.href === window.location.href) {
                link.classList.add("active");
                link.setAttribute("aria-current", "page");
            }
        });
        document.querySelectorAll(".dropdown-item").forEach((link) => {
            if (link.href === window.location.href) {
                link.classList.add("active");
                link.setAttribute("aria-current", "page");
            }
        });
    });

// Once a comment is added, the page scrolls down to a new comment
window.onload = function() {
    let comment_flag = localStorage.getItem("CommentsFlag");
    if (comment_flag) {
        console.log("Comment flag found")
        document.querySelector(comment_flag).scrollIntoView();
        localStorage.clear();
    }
    else {
        console.log("Comment flag not found")
    }
};