const WebSocket = require('ws').WebSocket;
const DerivAPI = require('@deriv/deriv-api/dist/DerivAPI');


const connection = new WebSocket('wss://ws.binaryws.com/websockets/v3?app_id=1089');

const api = new DerivAPI({ connection })
const basic = api.basic
basic.ping().then(console.log)

// const ticks = await api.ticks('R_100')
// ticks.onUpdate(tick => console.log(tick))
;(async function () {
  const ticks = await api.ticks('R_100')
  // ticks.onUpdate(tick => console.log(tick))
  ticks.onUpdate().subscribe(tick => console.log(tick))
})()

function Deque()
{
 this.stac=new Array();
 this.popback=function(){
  return this.stac.pop();
 }
 this.pushback=function(item){
  this.stac.push(item);
 }
 this.popfront=function(){
  return this.stac.shift();
 }
 this.pushfront=function(item){
  this.stac.unshift(item);
 }
}
