const wrapper = document.querySelector('.wrapper1');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=> {
  wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
  wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
  wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
  wrapper.classList.remove('active-popup');
});

    // Select all buttons and the checkbox
const buttons = document.querySelectorAll('button');
const checkbox = document.getElementById('hbm');
const links = document.querySelectorAll('a');

// Add click event listeners to all buttons
buttons.forEach(button => {
  button.addEventListener('click', () => {
    checkbox.checked = false; // Uncheck the checkbox
  });
});

links.forEach(link => {
  link.addEventListener('click', () => {
    checkbox.checked =false;
  })
})