import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";

import IfttLogo from '../../../../assets/authenticationLogo/font-style.png';

const NewPassword = () => {
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const { height } = useWindowDimensions();
    const Navigation = useNavigation();
    
    const SignSubmitPressed = () => {
        Navigation.navigate("Sign In");
    }

    const loginPressed = () => {
        Navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgNewForgotPass}>
        <Image
                    source={IfttLogo}
                    style={[styles.IftttLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
            />
                <View style={styles.NewPasswordContainer}>
                    <Text style={styles.NewPasswordTitle}>Add New password</Text>
                    <CustomerInput
                    placeholder="Enter you verification code"
                    value={code}
                    setValue={setCode}
                    secureTextEntry={false}
                    />
                    <CustomerInput
                    placeholder="Enter your new password"
                    value={newPassword}
                    setValue={setNewPassword}
                    secureTextEntry={false}
                    />
                    <CustomerButton text="Submit" onPress={SignSubmitPressed} bgColor={""} fgColor={""}/>

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
    bgNewForgotPass: {
        top: 20,
        marginTop: 20,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#F5F5F5',
    },
    NewPasswordContainer: {
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
    NewPasswordTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        margin: 10,
    },
})

export default NewPassword;