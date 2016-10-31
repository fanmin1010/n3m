import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';
import {List, ListItem} from 'material-ui/List';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import Avatar from 'material-ui/Avatar';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';
import { bindActionCreators } from 'redux';
import {grey400, darkBlack, lightBlack} from 'material-ui/styles/colors';

import * as actionCreators from '../../actions/auth';

function mapStateToProps(state) {
  return {
    token: state.auth.token,
    userName: state.auth.userName,
    isAuthenticated: state.auth.isAuthenticated
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}


const style = {
  height: '95%',
	overflow: 'hidden',
};
  

@connect(mapStateToProps, mapDispatchToProps)
export class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
      party: {name: 'Clark Kent'},
      messages: [
        {username: 'Clark Kent', avatar: 'dist/images/avatar03.png',  text: 'example message 1', time: '12:10:25p'},
        {username: 'Me', avatar: 'dist/images/default_avatar.png',  text: 'example message 2', time: '12:10:35p'},
        {username: 'Clark Kent', avatar: 'dist/images/avatar03.png',  text: 'example message 3', time: '12:11:11p'},
        {username: 'Me', avatar: 'dist/images/default_avatar.png',  text: 'example message 4', time: '12:11:36p'},
        {username: 'Clark Kent', avatar: 'dist/images/avatar03.png',  text: 'example message 5', time: '12:11:59p'},
        {username: 'Me', avatar: 'dist/images/default_avatar.png',  text: 'example message 6', time: '12:15:17p'},
      ],
      userName: props.userName,
    };

  }
  render() {
    return (
            <div className="col-md-8 col-md-offset-2" onKeyPress={(e) => this._handleKeyPress(e)}>
							<Paper style={style} zDepth={5} rounded={false} >
                <Subheader>{this.state.party.name}</Subheader>
                <Divider />
                <List  id="messagelist" style={{zIndex: '1', height: '85%', width: '98%', left: '1%', position: 'relative', overflow: 'scroll', }} >
								{this.state.messages.map(function(msg){
									return <ListItem
														leftAvatar={(msg.username === 'Me') ? null : <Avatar src={msg.avatar} />}
														rightAvatar={(msg.username === 'Me') ? <Avatar src={msg.avatar} /> : null}
														primaryText={
                              <h5>
															  <span style={{fontSize: '10pt', color: darkBlack}}>{msg.time} </span>-- 
                                {msg.username}
                              </h5>
                            }
                              secondaryText={
															<p>
																{msg.text} 
															</p>
														}
														secondaryTextLines={2}
														style={(msg.username === 'Me') ? {textAlign: 'right',} : {}}
													/>
								})}
                </List>

								<TextField
									hintText="Chat message"
                  id='chatinput'
									style={{width: '98%', left: '1%', position: 'relative', backgroundColor: 'white', bottom: '5px', zIndex: '2',}}
								/>	
							</Paper>
						</div>
        );
  }

  getMessage() {
    var msg = document.getElementById('chatinput').value;
    document.getElementById('chatinput').value = '';
    return msg;
  }

  sendMessage(msg) {
    console.log('send message: ' + msg);
    this.props.send_chat(msg, this.state.party.name);
    var messages = this.state.messages.slice();
    var newelement = {username: 'Me', avatar: 'dist/images/default_avatar.png',  text: msg, time: new Date().toTimeString().split(' ')[0]};
    messages.push(newelement);
    this.setState({ messages: messages }, () => {
      var m  = document.getElementById('messagelist');
      m.scrollTop = 9999;
    });
  }

  _handleKeyPress(e) {
    if (e.key === 'Enter') {
      var message = this.getMessage();
      this.sendMessage(message);
      debugger;
    }
  }
}

Chat.propTypes = {
  send_chat: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};

