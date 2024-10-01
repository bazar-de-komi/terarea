import React from "react";
import {View} from 'react-native';
import CustomerButton from "../CustomerButton";
// import GoogleLogo from '../../../assets/authenticationLogo/google.png';

const SocialSingInButton = () => {
    const SignInGoogle = () => {
        console.warn("Sing In Google");
    }

    const SignInGithub = () => {
        console.warn("Sing In Github");
    }

    return (
        <View>
            {/* <View style={styles.logoButtonContainer}> */}
                {/* <Image source={GoogleLogo} style={styles.logo} /> */}
                <CustomerButton
                text="Sign in with Google"
                onPress={SignInGoogle}
                bgColor="#FAE9EA"
                fgColor="#DD4D44"
                />
            {/* </View> */}
            <CustomerButton text="Sign in with GitHub" onPress={SignInGithub} bgColor="#e3e3e3" fgColor="#363636"/>
        </View>
    );
};

export default SocialSingInButton;