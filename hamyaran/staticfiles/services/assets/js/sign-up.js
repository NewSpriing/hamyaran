const nextButton = document.querySelector('.btn-next');
const pervButton = document.querySelector('.btn-prev');
const steps = document.querySelectorAll('.step');
const form_steps = document.querySelectorAll('.form-step');
let active = 1;

nextButton.addEventListener('click', () => {
  active++;
  if (active > steps.length) {
    active = steps.length;
  }
  updateProgress();
})

pervButton.addEventListener('click', () => {
  active++;
  if (active > 1) {
    active = 1;
  }
  updateProgress();
})

const updateProgress = () => {
  console.log('steps.length =>' + steps.length);
  console.log('active =>' + active);

  //toggle .active class for each list item
  steps.forEach((step, i) => {
    if (i == (active-1)) {
      step.classList.add('active');
      form_steps[i].classList.add('active');
      console.log('i =>' +i);
    } else {
        step.classList.remove('active');
        form_steps[i].classList.remove('active');
    }
  });

  //enable or disable prev and next button

  if (active === 1) {
      pervButton.disabled = true;
  } else if (active === steps.length) {
      nextButton.disabled = true;
  } else {
      pervButton.disabled = false;
      nextButton.disabled = false;
  }
}