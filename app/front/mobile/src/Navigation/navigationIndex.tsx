import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'

import SignIn from '../screens/Authentication/SignIn/signIn';
import SignUp from '../screens/Authentication/SignUp/signUp';
import ForgotPassword from '../screens/Authentication/ForgotPassword';
import NewPassword from '../screens/Authentication/ForgotPassword/newPassword';
import All from '../screens/Home/all';
import Applets from '../screens/Applets/appletsHome';
import Services from '../screens/Services/services';
import Start from '../screens/Start/start';
import AppletsScreen from '../screens/Applets/appletsBox';
import ServicesScreen from '../screens/Applets/createAppletServicesScreen';
import ServicesDetails from '../screens/Services/servicesDetails';
import Create from '../screens/Create/Home/create';
import CreateTwo from '../screens/Create/createServices';
import ChooseServicesTrigger from '../screens/Create/chooseServicesTrigger';
import ChooseServicesAction from '../screens/Create/chooseServicesAction';
import AppletsInformation from '../screens/Applets/appletsInformation';
import ChooseServicesOptionsForTrigger from '../screens/Create/chooseServicesOptionsForTrigger';
import ChooseServicesOptionsForAction from '../screens/Create/chooseServicesOptionsForAction'; 
import { OAuthScreen } from '../screens/Authentication/OAuth/oauth';
import Profile from '../screens/UserSideBar/sideBarProfil';
import DateTimeTrigger from '../screens/Create/CreateTrigger';
// import CreateAction from '../screens/Create/createAction';
import createAction from '../screens/Create/createAction';
import CreateAndHaveService from '../screens/Create/Home/createAndHaveService';
import CreateEnd from '../screens/Create/Home/createEnd';

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

                <Stack.Screen name="All" component={All} />
                <Stack.Screen name="Applets" component={Applets} />
                <Stack.Screen name="Services" component={Services} />

                <Stack.Screen name="Applet screen" component={AppletsScreen} />
                <Stack.Screen name="Service screen" component={ServicesScreen} />
                <Stack.Screen name="Service details" component={ServicesDetails} />
                <Stack.Screen name="Applets information" component={AppletsInformation} />            

                <Stack.Screen name="Create" component={Create} />
                <Stack.Screen name="Choose services trigger" component={ChooseServicesTrigger} />
                <Stack.Screen name="Choose services action" component={ChooseServicesAction} />
                <Stack.Screen name="Choose options service for trigger" component={ChooseServicesOptionsForTrigger} />
                <Stack.Screen name="Choose options service for action" component={ChooseServicesOptionsForAction} />
                <Stack.Screen name="Create two" component={CreateTwo} />
                <Stack.Screen name="Date time trigger" component={DateTimeTrigger} />
                <Stack.Screen name="Create action" component={createAction} />
                <Stack.Screen name="Create and have service" component={CreateAndHaveService} />
                <Stack.Screen name="Create end" component={CreateEnd} />

                <Stack.Screen name="Profile" component={Profile} />

            </Stack.Navigator>
        </NavigationContainer>
    )
}

export default Navigation
