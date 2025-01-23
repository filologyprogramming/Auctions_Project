
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

// Wait for all content to be loaded
document.addEventListener("DOMContentLoaded", function() {
    
// Look for different elements on a page

    // Look for "Add to watchlist form"
    let add_to_watchlist = document.querySelector("#add_to_watchlist_form");
        if (add_to_watchlist){
            add_to_watchlist.addEventListener("submit", handleAddToWatchlist);
        }    

    // Look for "Add a comment form"
    let add_comment = document.querySelector("#add_comment_form");
    if (add_comment) {
        add_comment.addEventListener("submit", handleAddComment);
    }

    // Look for a price form
    let price_form = document.querySelector("#place_a_bid_form");
    if (price_form) {
        price_form.addEventListener("submit", handlePlaceABid);
        }
    
    // Look for all remove from watchlist from in watchlist.html
    let remove_from_watchlist = document.querySelectorAll(".remove_from_watchlist");
    if (remove_from_watchlist) {
        for (let i = 0; i < remove_from_watchlist.length; i++) {
            remove_from_watchlist[i].addEventListener("submit", handleRemoveFromWatchlist);
            }
    }
    
    // Look for categories form
    let categories = document.querySelector("#categories_form");
    if (categories) {
        // Get the option user interacts with
        let selected_category = document.querySelector("#selected_category");
        // Handle category change
        selected_category.addEventListener("change", handleCategoryChoice);
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

function handleAddToWatchlist(event) {

    // Prevent event(submission)
    event.preventDefault();
        
    // Get ID of listing
    let listing_id = document.querySelector(".listing_id").value;
    console.log(listing_id);
                
    // Get value of a button - "Add..." or "Remove..."
    let input = document.querySelector("#add_to_watchlist");
    console.log(input);
    
    // Async function to add a listing to watchlist
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
    // Async function to remove a listing from watchlist
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
}
      
function handleAddComment(event) {

    // Block submision (adding a comment)
    event.preventDefault();
  
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
}

function handlePlaceABid(event) {

    // Block submision (place a bid)
    event.preventDefault();
                
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
}

function handleRemoveFromWatchlist(event) {
    
    // Block submission on each button
    event.preventDefault();
                
    // Find a child with ID of listing_id from the form which was just clicked/submitted
    let listing_id = event.target.querySelector(".listing_id").value;
    
    // Sent listing ID to view
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
        listing = document.querySelector(`#listing_${listing_id}`);
        listing.remove();
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}

function handleCategoryChoice(event) {
    // Deletes all listings - works like a web refresh without refreshing
    // Find the parent in the html
    let parent_element = document.querySelector(".all_listings");
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

            // Choose a grandparent
            let all_listings = document.querySelector(".all_listings");

            // Create a parent (listing)
            let parent = document.createElement("div");
            all_listings.appendChild(parent);
            parent.className = "listing"
            
            // Create first child (link)
            let child = document.createElement("a");
            parent.appendChild(child);
            let listing_id = data.listings[i].id;
            let listing_name = data.listings[i].name;
            child.setAttribute('href', `/${listing_id}/${listing_name}`);

            
            // Create child of child (imagebox)
            let image_box = document.createElement("div");
            child.appendChild(image_box);
            image_box.className = "image_box"
        

            // Create nameprice box
            let nameprice_box = document.createElement("div");
            child.appendChild(nameprice_box);
            nameprice_box.className = "nameprice_box"

            // Add picture
            let image = document.createElement("img");
            image_box.appendChild(image);
            let image_url = data.listings[i].image;
            let image_description = data.listings[i].description;

            // Add the source to the picture
            image.setAttribute('src', `${image_url}`);
            image.setAttribute('srcset', `"{{ listing.image_thumbnail.url }} 200w, 
                                        {{ listing.image_medium.url }} 350w,
                                        {{ listing.image_large.url }} 500w"`);
            image.setAttribute('alt', `${image_description}`);
            image.setAttribute('sizes', "(max-width: 480px) 100vw, (max-width: 800px) 50vw")
            
            // Create tags for paragraphs
            name_paragraph = document.createElement("p");
            price_paragraph = document.createElement("p");
            nameprice_box.appendChild(name_paragraph);
            nameprice_box.appendChild(price_paragraph);
            name_paragraph.className = "listing-name";
            price_paragraph.className = "listing-price"
            name_paragraph.textContent = data.listings[i].name;
            price_paragraph.textContent = "PLN " + data.listings[i].price;
        
        }
        // Change the url
        // history.pushState(null, null, `categories/${selected_category.value}`)
    })
    .catch(error => {
        console.log("Error", error);
    });
}