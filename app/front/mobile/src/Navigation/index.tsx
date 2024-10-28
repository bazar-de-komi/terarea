import  React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'

import SignIn from '../screens/Authentication/SignIn/signIn';
import SignUp from '../screens/Authentication/SignUp/signUp';
import ConfirmEmail from '../screens/Authentication/ConfirmEmail/ConfirmEmail';
import ForgotPassword from '../screens/Authentication/ForgotPassword';
import NewPassword from '../screens/Authentication/ForgotPassword/newPassword';
import All from '../screens/Home/all';
import Applets from '../screens/Home/applets';
import Services from '../screens/Home/services';
import Start from '../screens/Start/start';
import AppletsScreen from '../screens/AppletsScreen/AppletsScreen';
import ServicesScreen from '../screens/AppletsScreen/ServicesScreen';
import ServicesDetails from '../screens/AppletsScreen/ServicesDetails';
import Create from '../screens/Create/create';
import ChooseServices from '../screens/Create/chooseServices';
import BackButton from '../components/BackButton/backButton';

const Stack = createStackNavigator();

const Navigation = () => {
    return (
        <NavigationContainer>
            <Stack.Navigator screenOptions={{headerShown: false}}>
                <Stack.Screen name="Start" component={Start} />
                <Stack.Screen name="Sign Up" component={SignUp} />
                <Stack.Screen name="Sign In" component={SignIn} />
                <Stack.Screen name="Confirmation email" component={ConfirmEmail} />
                <Stack.Screen name="Forgot password" component={ForgotPassword} />
                <Stack.Screen name="New password" component={NewPassword} />

                <Stack.Screen name="All" component={All} />
                <Stack.Screen name="Applets" component={Applets} />
                <Stack.Screen name="Services" component={Services} />

                <Stack.Screen name="Applet screen" component={AppletsScreen} />
                <Stack.Screen name="Service screen" component={ServicesScreen} />
                <Stack.Screen name="Service details" component={ServicesDetails} />
                
                <Stack.Screen name="Back button" component={BackButton} />

                <Stack.Screen name="Create" component={Create} />
                <Stack.Screen name="Choose services" component={ChooseServices} />

            </Stack.Navigator>
        </NavigationContainer>
    )
}

export default Navigation