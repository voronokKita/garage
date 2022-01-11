/* code reminders */

const city = 'New York City'
console.log(logCitySkyline ());
function logCitySkyline () {
  let skyscraper = 'Empire State Building';
  return 'The stars over the ' + skyscraper + ' in ' + city;
}

const satellite = 'The Moon';
const galaxy = 'The Milky Way';
let stars = 'North Star';
console.log(callMyNightSky());
console.log(stars);
function callMyNightSky () {
  stars = 'Sirius';
  return 'Night Sky: ' + satellite + ', ' + stars + ', and ' + galaxy;
}

logVisibleLightWaves()
function logVisibleLightWaves() {
  const lightWaves = 'Moonlight';
  console.log(lightWaves);
}

const logVisibleLightWaves = () => {
  let lightWaves = 'Moonlight';
	let region = 'The Arctic';
  if (region === 'The Arctic') {
    let lightWaves = 'Northern Lights';
    console.log(lightWaves);
  }
  console.log(lightWaves);
};
logVisibleLightWaves();
