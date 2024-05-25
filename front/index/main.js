document.addEventListener('DOMContentLoaded', () => {
   const navMenu = document.getElementById('nav-menu'),
         navToggle = document.getElementById('nav-toggle'),
         navClose = document.getElementById('nav-close');

   if (navToggle) {
       navToggle.addEventListener('click', () => {
           if (navMenu) {
               navMenu.classList.add('show-menu');
           }
       });
   }

   if (navClose) {
       navClose.addEventListener('click', () => {
           if (navMenu) {
               navMenu.classList.remove('show-menu');
           }
       });
   }

   const search = document.getElementById('search'),
         searchBtn = document.getElementById('search-btn'),
         searchClose = document.getElementById('search-close');

   if (searchBtn) {
       searchBtn.addEventListener('click', () => {
           if (search) {
               search.classList.add('show-search');
           }
       });
   }

   if (searchClose) {
       searchClose.addEventListener('click', () => {
           if (search) {
               search.classList.remove('show-search');
           }
       });
   }

   const login = document.getElementById('login'),
         loginBtn = document.getElementById('login-btn'),
         loginClose = document.getElementById('login-close');

   if (loginBtn) {
       loginBtn.addEventListener('click', () => {
           if (login) {
               login.classList.add('show-login');
           }
       });
   }

   if (loginClose) {
       loginClose.addEventListener('click', () => {
           if (login) {
               login.classList.remove('show-login');
           }
       });
   }
});
