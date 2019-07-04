// pre_load img
var img = new Image();
img.onload=()=>{ alert('ok')};  
img.onerror=function(){};  
img.src= picurl; 

// countup.js
https://inorganik.github.io/countUp.js/
let countUpWait = new CountUp('countup_wait', 333251, {duration:3});
