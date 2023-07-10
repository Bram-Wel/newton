import DerivAPIBasic from 'https://cdn.skypack.dev/@deriv/deriv-api/dist/DerivAPIBasic';
/*
 * The module gets the most recent tick-hostory
 * before subscribing to a tick stream by symbol.
 *
 * */

const app_id = 36821 // Default 1089
const connection = new WebSocket(`wss://ws.binaryws.com/websockets/v3?app_id=${app_id}`);
const api = new DerivAPIBasic({ connection });

const select = document.getElementById("derivatives");
let previous_symbol;
;(function () {
  $("select").on('focus', function () {
    // Store the current value on focus and on change
    previous_symbol = this.value;
  }).change(function() {
      // Do something with the previous value after the change
      //alert(previous_symbol);
      // Make sure the previous value is updated
      previous_symbol = this.value;
    });
})();
select.addEventListener('change', function handleChange(event) {
  // console.log(select.options[select.selectedIndex].value);
  unsubscribeTicks()
    .then(() => {
      ticks_request.ticks_history = event.target.value // symbol
      // console.error(ticks_request);
      return forgetTicks();
    })
    .then(() => Promise.all([getTicksHistory(), subscribeTicks()]))
    .catch((err) => console.error(err));
});
const tickCount = document.getElementById("tick_count")
tickCount.addEventListener('change', function handleChange(event) {
  //console.log(event.target.value)
  //console.log(tickCount.value)
  unsubscribeTicks()
    .then(() => {
      ticks_history_request.count = Number(event.target.value)
      ticks_request.count = ticks_history_request.count
      // console.error(ticks_request)
      return forgetTicks()
    })
    .then(() => Promise.all([getTicksHistory(), subscribeTicks()]))
    .catch((error) => console.error(error));
});
// console.log(`Ticks: ${tickCount.value}`)

const ticks_history_request = {
  ticks_history: select.options[select.selectedIndex].value, // symbol
  adjust_start_time: 1,
  count: Number(tickCount.value),// length of tick history by tick
  end: 'latest',
  start: 1,
  style: 'ticks',
};
const ticks_request = {
  ...ticks_history_request,
  subscribe: 1,
};

function percentages(array) {
  let count = 0, odd = 0, even = 0;
  array.map((price) => {
    if (Number(String(price).at(-1)) % 2) {
    // if ((price * 1000) % 2) {
      //console.log(`Odd: ${price}`)
      count += 1;
      odd += 1;
    } else {
      //console.log(`Even: ${price}`)
      even += 1;
    }
    return;
  });
  //console.log(`Array: ${count}`)
  const sum = odd + even
  document.getElementById("even").innerHTML = `Even: ${((even/sum) * 100).toFixed(1)} Ticks: ${array.length - count}`
  document.getElementById("odd").innerHTML = `Odd: ${((odd/sum) * 100).toFixed(1)} Ticks: ${count}`
  const data = [
    {
      x: ["Even Digit", "Odd Digit"],
      y: [((even/sum) * 100).toFixed(1), ((odd/sum) * 100).toFixed(1)],
      name: ticks_request.ticks_history,
      marker: {
        bgcolor: 'rgba(24, 24, 32, 1)',
        color: ['rgba(66, 233, 138, 0.6)', 'rgba(178, 119, 103, 0.6)']
      },
      // bgcolor: 'rgba(24, 24, 32, 1)',
      width: [0.4, 0.4],
      type: "bar",
    }
  ];
  Plotly.newPlot("graph", data)
};

function Deque() {
  this.stac=new Array();
  this.popback=function() {
    return this.stac.pop();
  }
  this.pushback=function(item) {
    this.stac.push(item);
  }
  this.popfront=function() {
    return this.stac.shift();
  }
  this.pushfront=function(item){
    this.stac.unshift(item);
  }
}
const ticksQueue = new Deque;

const tickSubscriber = () => api.subscribe(ticks_request);
async function forgetTicks() {
  return await api.forgetAll("ticks")
}
const ticksHistoryResponse = async (res) => {
  const data = JSON.parse(res.data);
  if (data.error !== undefined) {
    //connection.removeEventListener('message', ticksHistoryResponse, false);
    //await api.disconnect();
    if (data.error.message === 'This market is presently closed.') {
      let symbol = $('#symbols').data().name.filter((item) => item.symbol === ticks_request.ticks_history)[0].display_name
      document.getElementById('Modal-MarketClosed').getElementsByClassName('modal-title')[0].innerHTML = symbol;
      document.getElementById('Modal-MarketClosed').getElementsByClassName('modal-body')[0].innerHTML = data.error.message;
      $('#Modal-MarketClosed').modal('show');
      ticks_request.ticks_history = previous_symbol;
    } else {
      alert(data.error.message)
    }
  }
  if (data.msg_type === 'history') {
    ticksQueue.stac.length = 0;
    data.history.prices.forEach(price => ticksQueue.pushback(price))
    //console.log(ticksQueue)
    console.log(data.history);
  }
  connection.removeEventListener('message', ticksHistoryResponse, false);
};
const ticksResponse = async (res) => {
  const data = JSON.parse(res.data);
  // This example returns an object with a selected amount of past ticks.
  if (data.error !== undefined) {
    // alert(data.error.message);
    console.error(data.error.message)
    // connection.removeEventListener('message', ticksResponse, false);
    // await api.disconnect();
  }
  // Allows you to monitor ticks.
  if (data.msg_type === 'tick') {
    ticksQueue.pushback(data.tick.quote);
    ticksQueue.popfront();
    console.log(data.tick);
    const currency = document.getElementById("quote").innerHTML.trim().slice(-3)
    document.getElementById("quote").innerHTML = data.tick.quote.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",").concat(' ', currency);
    percentages(ticksQueue.stac);
  }
};
const subscribeTicks = async () => {
  connection.addEventListener('message', ticksResponse);
  return await tickSubscriber();
};
const unsubscribeTicks = async () => {
  connection.removeEventListener('message', ticksResponse, false);
  return await tickSubscriber().unsubscribe();
};
const getTicksHistory = async () => {
  connection.addEventListener('message', ticksHistoryResponse);
  return await api.ticksHistory(ticks_history_request);
};
getTicksHistory()
//  .then(() => ticksQueue.stac.forEach((l) => console.log(l)));
subscribeTicks()
