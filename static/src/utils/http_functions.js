/* eslint camelcase: 0 */
/* global socket */
import axios from 'axios';

const tokenConfig = (token) => ({
  headers: {
    'Authorization': token, // eslint-disable-line quote-props
  },
});

export function validate_token(token) {
  return axios.post('/api/is_token_valid', {
    token,
  });
}

export function create_user(username, email, password, pgp_key) {
  return axios.post('api/create_user', {
    username,
    email,
    password,
    pgp_key,
  });
}

export function addFriendCall(email, token, cb) {
  return axios.post('api/user_add_friend', {
    email: email, 
  }, tokenConfig(token))
  .then(cb)
  .catch((error) => {
    console.log(error);
  });
}

export function addPartyCall(partyName, token, cb) {
  return axios.post('api/createParty', {
    partyName: partyName, 
  }, tokenConfig(token))
  .then(cb)
  .catch((error) => {
    console.log(error);
  });
}

export function get_token(email, password) {
  return axios.post('api/get_token', {
    email,
    password,
  });
}

export function data_about_user(token) {
  return axios.get('api/user', tokenConfig(token));
}

export function friendlistCall(token, cb) {
  return axios.get('api/friendlist', tokenConfig(token))
            .then(cb)
            .catch((error) => {
              console.log(error);
            });
}

export function friendHistoryCall(friendName, token, cb) {
  return axios.post('api/friendhistory', {
      'friend': friendName
    }, tokenConfig(token))
            .then(cb)
            .catch((error) => {
              console.log(error);
            });
}
/**
 * @param msg {string} message text of chat
 * @param pname {string} party name
 * @param pid {string} party id
 * @param uname {string} user name
 * @param cb {Funtion} call back function
 **/
export function socket_party_msg(msg, pname, pid, uname, cb) {
  console.log('inside socket_party_msg');
  console.log(msg);
  console.log(pname);
  console.log(pid);
  console.log(uname);
  console.log(cb);
  socket.emit('party_message', { msgtext: msg, partyname: pname, partyId: pid, username: uname }, cb);
}


export function partylistCall(token, cb) {
  return axios.get('api/partylist', tokenConfig(token))
            .then(cb)
            .catch((error) => {
              console.log(error);
            });
}

/**
 * @param msg {string} message text of chat
 * @param pname {string} party name
 * @param receiver {string} the username to whome the message is being directed.
 * @param sender {string} user name
 * @param cb {Funtion} call back function
 **/
export function socket_msg(msg, pname, receiver, sender, cb) {
  console.log('inside socket_msg');
  console.log('Party: ' + pname);
  console.log('From: ' + sender);
  console.log('To: ' + receiver);
  console.log('Body: ' + msg);
  socket.emit('user2user_message', { msgtext: msg, partyname: pname, receiver: receiver, sender: sender }, cb);
}


export function callUberCall(addr) {
  return axios.post('api/calluber',{
    'end_address': addr
  });
}

export function callOpenTableCall(id, covers, datetime) {
  return axios.post('api/callopentable',{
    'id': id,
    'covers': covers,
    'datetime': datetime
  });
}
