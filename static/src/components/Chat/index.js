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
	margin: '15px 0 0px',
	overflow: 'hidden',
};
  

@connect(mapStateToProps, mapDispatchToProps)
export class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
      party: {name: 'Clark Kent'},
      messages: [
        {username: 'Clark Kent', avatar: 'dist/images/avatar3.png',  text: 'example message 1', time: '12:10:25p'},
        {username: 'Me', avatar: 'dist/images/avatar5.png',  text: 'example message 2', time: '12:10:35p'},
        {username: 'Clark Kent', avatar: 'dist/images/avatar3.png',  text: 'example message 3', time: '12:11:11p'},
        {username: 'Me', avatar: 'dist/images/avatar5.png',  text: 'example message 4', time: '12:11:36p'},
        {username: 'Clark Kent', avatar: 'dist/images/avatar3.png',  text: 'example message 5', time: '12:11:59p'},
        {username: 'Me', avatar: 'dist/images/avatar5.png',  text: 'example message 6', time: '12:15:17p'},
      ]
    };

  }

  render() {
    return (
            <div className="col-md-8 col-md-offset-2" >
							<Paper style={style} zDepth={5} rounded={false} >
                <Subheader>{this.state.party.name}</Subheader>
                <Divider />
                <List  style={{zIndex: '1', position: 'absolute', height: '85%', width: '100%', overflow: 'scroll', }} >
								{this.state.messages.map(function(msg){
									return <div>
													<ListItem
														leftAvatar={(msg.username === 'Me') ? null : <Avatar src={msg.avatar} />}
														rightAvatar={(msg.username === 'Me') ? <Avatar src={msg.avatar} /> : null}
														primaryText={msg.username}
														secondaryText={
															<p>
																<span style={{color: darkBlack}}>{msg.time}</span> --
																{msg.text} 
															</p>
														}
														secondaryTextLines={2}
														style={(msg.username === 'Me') ? {textAlign: 'right', margin: '0 35px',} : {}}
													/>
													<Divider />
													</div>
								})}
                </List>

								<TextField
									hintText="Chat message"
									style={{width: '94%', position: 'absolute', bottom: '0', left: '19px', zIndex: '2',}}
								/>	
							</Paper>
						</div>
        );
  }
}

Chat.propTypes = {
  logoutAndRedirect: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool,
};

