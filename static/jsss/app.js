formSection = document.querySelector('.wholesales-customer-info')

console.log(formSection)

/* For the wholesale's(wholesale.html) hidden display */

let customerName = document.querySelector("#wholesales-customer-name")
let verifyRealCustomer = document.querySelector(".wholesales-submit-btn")
let wholesalesDisplay = document.querySelector(".wholesales-display")
let customerNameDisplay = document.querySelector(".wholesales-customer-name-value")
let exitContainer = document.querySelector(".wholesales-menu-exit-container")
let wholesalesPopup = document.querySelector(".wholesales-popup-container")
let wholesalesSellBtns = document.querySelectorAll(".wholesales-sell-btn")

let wholesalesPopupProductName = document.querySelector(".wholesales-popup-product-name")
let wholesalesPopupSubmit = document.querySelector(".wholesales-popup-submit")
let wholesalesPopupProductPrice = document.querySelector(".wholesales-popup-product-price")

let wholesalesCalculateBtn = document.querySelector(".wholesales-calculate-btn")

let productName = document.querySelectorAll(".wholesales-product-name")

let itemspurchased = {}

/* To display product and customer name */
verifyRealCustomer.addEventListener('click', function() {
    if(wholesalesDisplay.classList.contains("wholesales-product-display-hide")) {
        wholesalesDisplay.classList.remove("wholesales-product-display-hide")
        customerNameDisplay.innerHTML = customerName.value
    }
})


/* To display items to sell */

wholesalesSellBtns.forEach(function(wholesalesSellBtn) {
    wholesalesSellBtn.addEventListener('click', function(e) {
        let itemName = e.currentTarget.parentElement.querySelector(".wholesales-product-name")
        let itemPrice = e.currentTarget.parentElement.querySelector(".wholesales-item-price")
        wholesalesPopupProductName.textContent = itemName.textContent
        wholesalesPopupProductPrice.innerHTML = itemPrice.textContent
        if(wholesalesPopup.classList.contains("wholesales-hidden")) {
            wholesalesPopup.classList.remove("wholesales-hidden")
          }
    })
})


wholesalesPopupSubmit.addEventListener('click', function(e) {
    let nameOfItem = e.currentTarget.parentElement.querySelector(".wholesales-popup-product-name").innerText
    let productAmount = Number(e.currentTarget.parentElement.querySelector(".wholesales-popup-input").value)
    let productPrice = Number(e.currentTarget.parentElement.querySelector(".wholesales-popup-product-price").innerText)
    itemspurchased[nameOfItem] = [productAmount, productPrice]
    wholesalesPopup.classList.add("wholesales-hidden")
})


wholesalesCalculateBtn.addEventListener('click', function() {
    console.log(itemspurchased)
    localStorage.setItem(customerNameDisplay.innerText, JSON.stringify(itemspurchased))
})



exitContainer.addEventListener('click', function() {
    wholesalesPopup.classList.add("wholesales-hidden")
})





// const stockItems = document.querySelectorAll(".stock-item")

// stockItems.forEach(function(stockItem) {
//     stockItem.addEventListener("click", function(e) {
//             e.currentTarget.classList.add("stock-item-active")
//     })
// })















// (function() {
//     let mainMenuDisplay = document.querySelector('.main-nav-menu-container')
//     let mainMenuRemove = document.querySelector('.main-menu-exit-container')
//     let mainMenuTarget = document.querySelector('.main-menu-container')

//     mainMenuDisplay.forEach( (menuDisplay) => {
//         menuDisplay.addEventListener('click', () => {
//             if(mainMenuTarget.classList.contains('main-menu-hide')) {
//                 mainMenuTarget.classList.remove('main-menu-hide')
//             }
//             else {
//                 return False
//             }
//         })
//     })
// })
