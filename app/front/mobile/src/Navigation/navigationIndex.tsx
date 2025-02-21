import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'

import Start from '../screens/Start/start';
import SignIn from '../screens/Authentication/SignIn/signIn';
import SignUp from '../screens/Authentication/SignUp/signUp';
import ForgotPassword from '../screens/Authentication/ForgotPassword/forgotPassword';
import NewPassword from '../screens/Authentication/ForgotPassword/newPassword';
import { OAuthScreen } from '../screens/Authentication/OAuth/oauth';

import Applets from '../screens/Applets/appletsHome';
import AppletInformation from '../screens/Applets/appletInformation';

import Create from '../screens/Create/create';
import ChooseServicesTrigger from '../screens/Create/chooseServicesTrigger';
import ChooseServicesAction from '../screens/Create/chooseServicesAction';
import ChooseServicesOptionsForTrigger from '../screens/Create/chooseServicesOptionsForTrigger';
import ChooseServicesOptionsForAction from '../screens/Create/chooseServicesOptionsForAction';
import CreateTrigger from '../screens/Create/createTrigger';
import CreateAction from '../screens/Create/createAction';

import Profile from '../screens/UserProfile/userProfile';

const Stack = createStackNavigator();

const Navigation = () => {
    return (
        <NavigationContainer>
            <Stack.Navigator screenOptions={{ headerShown: false }} detachInactiveScreens>
                <Stack.Screen name="Start" component={Start} />
                <Stack.Screen name="Sign Up" component={SignUp} />
                <Stack.Screen name="Sign In" component={SignIn} />
                <Stack.Screen name="Forgot password" component={ForgotPassword} />
                <Stack.Screen name="New password" component={NewPassword} />
                <Stack.Screen name="Oauth screen" component={OAuthScreen} />

                <Stack.Screen name="Applets" component={Applets} />
                <Stack.Screen name="Applet information" component={AppletInformation} />

                <Stack.Screen name="Create" component={Create} />
                <Stack.Screen name="Choose services trigger" component={ChooseServicesTrigger} />
                <Stack.Screen name="Choose services action" component={ChooseServicesAction} />
                <Stack.Screen name="Choose options service for trigger" component={ChooseServicesOptionsForTrigger} />
                <Stack.Screen name="Choose options service for action" component={ChooseServicesOptionsForAction} />
                <Stack.Screen name="Create trigger" component={CreateTrigger} />
                <Stack.Screen name="Create action" component={CreateAction} />

                <Stack.Screen name="Profile" component={Profile} />

            </Stack.Navigator>
        </NavigationContainer>
    )
}

export default Navigation
