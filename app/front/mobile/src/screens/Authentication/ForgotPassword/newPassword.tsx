import React, { useState } from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions, Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";
import { getValue, deleteKey } from "../../../components/StoreData/storeData";

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';
import { queries } from "../../../../back-endConnection/querier";

const NewPassword = () => {
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirm, setConfirm] = useState('');
    const { height } = useWindowDimensions();
    const navigation = useNavigation();

    const handleSignSubmitButton = async () => {
        if (newPassword !== confirm) {
            Alert.alert("The password and the confirm password must be the same.");
            return;
        }
        const newPass = {
            code: code,
            email: await getValue("email"),
            password: confirm,
        };

        try {
            console.log("NewPass:", newPass);
            const response = await queries.patch("/api/v1/reset_password", newPass);
            console.log("Response:", response);
            if (response.resp === "success") {
                deleteKey("email");
                navigation.navigate("Sign In");
            }
        } catch (error) {
            console.error("Error:", error);
            Alert.alert("One of the value is incorrect. Please try again.");
        }
    }

    const handleSendEmail = async () => {
        const email = await getValue("email")
        await queries.post("/api/v1/send_email_verification", { email })
        Alert.alert("A verification email was resend.");
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
                        value={confirm}
                        setValue={setConfirm}
                        secureTextEntry={false}
                    />
                    <CustomerButton
                        text="Set password"
                        onPress={() => handleSignSubmitButton()}
                        bgColor={"black"}
                        fgColor={""}
                    />
                    <CustomerButton
                        text="Resend verification email"
                        onPress={() => handleSendEmail()}
                        bgColor={'#6c63ff'}
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
