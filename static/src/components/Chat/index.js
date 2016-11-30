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
import {
    UBER_USERNAME,
    OPENTABLE_USERNAME,
    BOTLIST,
} from '../../constants/index';

function mapStateToProps(state) {
  console.log(state);
  return {
    token: state.auth.token,
    userName: state.auth.userName,
    isParty: state.chat.isParty,
    receiver: state.chat.receiver,
    avatar: state.auth.avatar,
    isAuthenticated: state.auth.isAuthenticated,
    partyname: state.chat.partyname,
    partyId: state.chat.partyId,
    messages: state.chat.messages,
    allMessages: state.chat.allMessages,
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
  }

  componentDidMount() {
  }

  componentWillMount() {
    this.props.setChatWindow(this.props.partyname);
    this.props.setNewListener(this.props.partyname);
  }

  render() {
    return (
            <div className="col-md-8 col-md-offset-2" onKeyPress={(e) => this._handleKeyPress(e)}>
							<Paper style={style} zDepth={5} rounded={false} >
                <Subheader>{this.props.partyname}</Subheader>
                <Divider />
                <List id="messagelist" style={{ zIndex: '1', height: '85%', width: '98%', left: '1%', position: 'relative', overflow: 'scroll' }} >
                {this.props.messages.map((msg) => {
                    return (<ListItem
                      leftAvatar={(msg.username === this.props.userName) ? null : <Avatar src={msg.avatar} />}
                      rightAvatar={(msg.username === this.props.userName) ? <Avatar src={msg.avatar} /> : null}
                      secondaryText={
                          <h5>
                            <span style={{ fontSize: '10pt', color: darkBlack }}>{msg.time} </span>--
                            {msg.username}
                          </h5>
                        }
                      primaryText={
                        (BOTLIST.includes(msg.username))
                          ? <pre> {msg.text} </pre>
                          : <p> {msg.text} </p>
                       }
                      secondaryTextLines={1}
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
    if(this.props.isParty) {
      this.props.send_party_chat(msg, this.props.partyname.replace(' ', ''), this.props.partyId, this.props.userName);
    } else {
      this.props.send_chat(msg, this.props.partyname.replace(' ', ''), this.props.receiver, this.props.userName);
      
    }
    document.getElementById('chatinput').value = '';
    if(OPENTABLE_USERNAME === this.props.partyname){
      document.getElementById('chatinput').placeholder = 'Restaurant Name@8:00pm';
    }
    else if(UBER_USERNAME === this.props.partyname){
      document.getElementById('chatinput').placeholder = 'Destination Address';
    }
    else {
      document.getElementById('chatinput').placeholder = 'Chat Message';
    }
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
  send_party_chat: React.PropTypes.func,
  setChatWindow: React.PropTypes.func,
  setNewListener: React.PropTypes.func,
  addMessage: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};
