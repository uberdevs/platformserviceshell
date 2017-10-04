const events = require('events');
const eventEmitter = new events.EventEmitter();

require('dotenv').config({ path: 'variables.env' });

console.log(`Application ${process.env.APPLICATION} is starting...`);

const app = require('./app');

app.set('port', process.env.PORT || 7777);
const server = app.listen(app.get('port'), () => {
  console.log(`Express running → PORT ${server.address().port}`);
  eventEmitter.emit('onStart');
});


// Application Event Handlers

var onStart = function () {
  // Do Initialization Work Here
  console.log(`Application ${process.env.APPLICATION} has started successfully.`);
}

var onStop = function () {
  console.log(`Application ${process.env.APPLICATION} has stopped successfully.`);
}

function exitHandler(options, err) {
  var signalStop = false;
  if (options.cleanup) {
    console.log(`Application ${process.env.APPLICATION} is stopping...`);
    signalStop = true;
    // Do Clean-Up Work Here
    console.log(`Application ${process.env.APPLICATION} has stopped.`);
  }

  if (err) {
    console.log(err.stack);
  }

  if (options.exit) {
    if(signalStop){
      console.log(`Application ${process.env.APPLICATION} has stopped.`);
    }

    process.exit();
  }
}

eventEmitter.on('onStart', onStart);

// Catches Application Closing
process.on('exit', exitHandler.bind(null,{cleanup:true}));

// Catches Ctrl+C Event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));