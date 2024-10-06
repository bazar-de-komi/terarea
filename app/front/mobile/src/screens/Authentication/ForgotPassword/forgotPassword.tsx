import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";

import IftttLogo from '../../../../assets/authenticationLogo/font-style.png'

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const { height } = useWindowDimensions();
    const navigation = useNavigation();

    const SignSendPressed = () => {
        console.warn("send");
        navigation.navigate("New password");
    }

    const loginPressed = () => {
        console.warn("Log in");
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgForgotPass}>
            <Image
                    source={IftttLogo}
                    style={[styles.IftttLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
            />
                <View style={styles.ForgotPasswordContainer}>
                    <Text style={styles.ForgotPasswordTitle}>Reset your password</Text>
                    <CustomerInput
                    placeholder="email"
                    value={email}
                    setValue={setEmail}
                    secureTextEntry={false}
                    />
                    <CustomerButton
                    text="Send"
                    onPress={SignSendPressed}
                    bgColor={""}
                    fgColor={""}
                    />
                    <CustomerButton
                    text="Back to Sign in"
                    onPress={loginPressed}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                    />

                </View>
        </View>
    </ScrollView>
    );
};

const styles = StyleSheet.create({
    bgForgotPass: {
        top: 20,
        marginTop: 20,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#F5F5F5',
    },
    ForgotPasswordContainer: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: '#e0d8d7',
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
    },
    IftttLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 100,
        marginBottom: 60,
    },
    ForgotPasswordTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        margin: 10,
    },
})

export default ForgotPassword;