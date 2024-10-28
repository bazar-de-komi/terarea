import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

const NewPassword = () => {
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const { height } = useWindowDimensions();
    const Navigation = useNavigation();
    
    const SignSubmitPressed = () => {
        Navigation.navigate("Sign In");
    }

    const SendEmail = () => {
        console.warn("send email");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgNewForgotPass}>
            <Image
                    source={AreaLogo}
                    style={[styles.areaLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
            />
                <View style={styles.NewPasswordContainer}>
                    <Text style={styles.NewPasswordTitle}>Reset your password</Text>
                    <CustomerInput
                    placeholder="Verification code"
                    value={code}
                    setValue={setCode}
                    secureTextEntry={false}
                    />
                    <CustomerInput
                    placeholder="New password"
                    value={newPassword}
                    setValue={setNewPassword}
                    secureTextEntry={false}
                    />
                     <CustomerInput
                    placeholder="Confirmation password"
                    value={newPassword}
                    setValue={setNewPassword}
                    secureTextEntry={false}
                    />
                    <CustomerButton
                    text="Set password"
                    onPress={SignSubmitPressed}
                    bgColor={"black"}
                    fgColor={""}
                    />
                    <CustomerButton
                    text="Resend verification email"
                    onPress={SendEmail}
                    bgColor={'#6c63ff'}
                    fgColor={""}
                    />

                    {/* <CustomerButton
                    text="Back to Sign in"
                    onPress={loginPressed}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                    /> */}
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
    areaLogo: {
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