/* code reminders */

for (let counter = 5; counter <= 10; counter++) {
  console.log(counter);
}

const vacationSpots = ['Bali', 'Paris', 'Tulum'];
for (let i = 0; i < vacationSpots.length; i++){
  console.log(`I would love to visit ${vacationSpots[i]}`);
}

let bobsFollowers = ['Alice', 'Bill', 'Cena', 'Dan'];
let tinasFollowers = ['Cena', 'Dan', 'Eleina'];
let mutualFollowers = [];
for (let i = 0; i < bobsFollowers.length; i++) {

  for (let j = 0; j < tinasFollowers.length; j++) {
    
    if (bobsFollowers[i] === tinasFollowers[j]) {

      mutualFollowers.push(bobsFollowers[i]);
}}}
console.log(mutualFollowers);

const cards = ['diamond', 'spade', 'heart', 'club'];
let currentCard;
while (currentCard != 'spade') {
  currentCard = cards[Math.floor(Math.random() * 4)];
  console.log(currentCard);
}

let cupsOfSugarNeeded = 9;
let cupsAdded = 0;
do {
  cupsAdded++;
  console.log(cupsAdded);
} while (cupsAdded < cupsOfSugarNeeded);

const rapperArray = ["Lil' Kim", "Jay-Z", "Notorious B.I.G.", "Tupac"];
for (let i = 0; i < rapperArray.length; i++) {
  
  console.log(rapperArray[i]);
  if (rapperArray[i] === 'Notorious B.I.G.') {break;}
}
console.log("And if you don't know, now you know.");
