import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { connect } from 'react-redux';
import { List, ListItem } from 'material-ui/List';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import Avatar from 'material-ui/Avatar';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';
import { bindActionCreators } from 'redux';
import { grey400, darkBlack, lightBlack } from 'material-ui/styles/colors';

import * as actionCreators from '../../actions/chat';

function mapStateToProps(state) {
  return {
    token: state.auth.token,
    userName: state.auth.userName,
    avatar: state.auth.avatar,
    isAuthenticated: state.auth.isAuthenticated,
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
      party: { name: 'Clark Kent' },
      messages: [
      ],
      userName: props.userName,
    };

  }

  componentDidMount() {
    socket.on(this.state.party.name.replace(' ', ''), this.receiveMessage.bind(this));
  }

  receiveMessage(data) {
      console.dir(data);
      const messages = this.state.messages.slice();
      const newelement = { username: data.username, avatar: data.avatar, text: data.msg, time: new Date().toTimeString().split(' ')[0] };
      messages.push(newelement);
      this.setState({ messages }, () => {
        const m = document.getElementById('messagelist');
        m.scrollTop = 9999;
        document.getElementById('chatinput').value = '';
      });
    }


  render() {
    return (
            <div className="col-md-8 col-md-offset-2" onKeyPress={(e) => this._handleKeyPress(e)}>
							<Paper style={style} zDepth={5} rounded={false} >
                <Subheader>{this.state.party.name}</Subheader>
                <Divider />
                <List id="messagelist" style={{ zIndex: '1', height: '85%', width: '98%', left: '1%', position: 'relative', overflow: 'scroll' }} >
								{this.state.messages.map((msg) => {
									return (<ListItem
  leftAvatar={(msg.username === this.state.userName) ? null : <Avatar src={msg.avatar} />}
  rightAvatar={(msg.username === this.state.userName) ? <Avatar src={msg.avatar} /> : null}
  primaryText={
                              <h5>
															  <span style={{ fontSize: '10pt', color: darkBlack }}>{msg.time} </span>--
                                {msg.username}
                              </h5>
                            }
  secondaryText={
															<p>
																{msg.text}
															</p>
														}
  secondaryTextLines={2}
  style={(msg.username === 'Me') ? { textAlign: 'right' } : {}}
         />);
								})}
                </List>

								<TextField
  hintText="Chat message"
  id="chatinput"
  style={{ width: '98%', left: '1%', position: 'relative', backgroundColor: 'white', bottom: '5px', zIndex: '2' }}
								/>
							</Paper>
						</div>
        );
  }

  getMessage() {
    const msg = document.getElementById('chatinput').value;
    return msg;
  }

  sendMessage(msg) {
    console.log(this.state);
    this.props.send_chat(msg, this.state.party.name.replace(' ', ''), this.state.userName);
  }

  _handleKeyPress(e) {
    if (e.key === 'Enter') {
      const message = this.getMessage();
      this.sendMessage(message);
    }
  }
}

Chat.propTypes = {
  send_chat: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};
