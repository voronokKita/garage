/* code reminders */

getReminder();
greetInSpanish();
sayThanks('Cole');
makeShoppingList();
console.log(costOfMonitors(5, 4));
console.log(plantNeedsWater('Tuesday'));
 
function getReminder() {
  console.log('Water the plants.');
}
function greetInSpanish() {
  console.log('Buenas Tardes.');
}

function sayThanks(name) {
  console.log('Thank you for your purchase ' + name + '! We appreciate your business.');
}

function makeShoppingList(item1='milk', item2='bread', item3='eggs'){
  console.log(`Remember to buy ${item1}`);
  console.log(`Remember to buy ${item2}`);
  console.log(`Remember to buy ${item3}`);
}

function costOfMonitors(rows, columns) {
  return monitorCount(rows, columns) * 200;
}
function monitorCount(rows, columns) {
  return rows * columns;
}

const plantNeedsWater = function(day) {
  return (day === 'Wednesday') ? true : false;
}
// const plantNeedsWater = day => day === 'Wednesday' ? true : false;

