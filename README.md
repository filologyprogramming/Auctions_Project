# Auctions_Project
An auction website based on CS50 project

## TODOs:
- make an app desktop-friendly
- add pagination

### Functionality

Main functionailty allows users to :
- register and log in
- browse index page
- post new listings
- sort listings by category
- view listing's details
- comment under listings
- place bids
- sell active listings to users
- add and remove items from watchlist
- look up active biddings
- look up purchased items

### Specification

Project utilizes following models which store following information:
- deafult Django user
- Listing (description, price, posting data, condition, category, image, seller, active field, sold to, sold for)
- Bid (bid, bidder, listing)
- Comment (comment, listing, date, commenter)
- Watchlist (user, listing)



