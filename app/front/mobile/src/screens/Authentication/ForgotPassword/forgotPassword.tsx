import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

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
                    source={AreaLogo}
                    style={[styles.areaLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
            />
                <View style={styles.ForgotPasswordContainer}>
                    <Text style={styles.ForgotPasswordTitle}>Forgot your password ?</Text>
                    <CustomerInput
                    placeholder="Your email adress"
                    value={email}
                    setValue={setEmail}
                    secureTextEntry={false}
                    />
                    <Text>We will send you a link to reset your password</Text>
                    {/* <CustomerButton
                    text="We will send you a link to reset your password"
                    onPress={loginPressed}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                    /> */}
                    <CustomerButton
                    text="Reset password"
                    onPress={SignSendPressed}
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
        padding: 20,
    },
    areaLogo: {
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