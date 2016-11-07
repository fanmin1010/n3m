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

export function get_token(email, password) {
  return axios.post('api/get_token', {
    email,
    password,
  });
}

export function data_about_user(token) {
  return axios.get('api/user', tokenConfig(token));
}

/**
 * @param msg {string} message text of chat
 * @param pname {string} party name
 * @param uname {string} user name
 * @param cb {Funtion} call back function
 **/
export function socket_msg(msg, pname, uname, cb) {
  console.log(msg);
  console.log(pname);
  console.log(uname);
  socket.emit('servermessage', { msgtext: msg, partyname: pname, username: uname }, cb);
}

