/* eslint new-cap: 0 */

import React from 'react';
import { Route } from 'react-router';

/* containers */
import { App } from './containers/App';
import { HomeContainer } from './containers/HomeContainer';
import LoginView from './components/LoginView';
import RegisterView from './components/RegisterView';
import NotFound from './components/NotFound';

import ProtectedView from './components/ProtectedView';
import About from './components/About';
import Chat from './components/Chat';
import ProfileView from './components/ProfileView';

import { DetermineAuth } from './components/DetermineAuth';
import { requireNoAuthentication } from './components/notAuthenticatedComponent';
import { requireAuthentication } from './components/AuthenticatedComponent';





export default (
    <Route path="/" component={App}>
        /* public routes */
        <Route path="login" component={requireNoAuthentication(LoginView)} />
        <Route path="register" component={requireNoAuthentication(RegisterView)} />
        <Route path="home" component={requireNoAuthentication(HomeContainer)} />

        /* private routes */
        <Route path="main" component={requireAuthentication(ProtectedView)} />
        <Route path="profile" component={requireAuthentication(ProfileView)} />
        <Route path="about" component={requireAuthentication(About)} />
        <Route path="chat" component={requireAuthentication(Chat)} />

        /* catch all */
        <Route path="*" component={DetermineAuth(NotFound)} />
    </Route>
);
