import React, { useState } from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions } from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomInput from "../../../components/CustomInput/customInput";
import CustomButton from "../../../components/CustomButton/customButton";
import { storeValue } from "../../../components/StoreData/storeData";

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';
import { queries } from "../../../../back-endConnection/querier";

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const { height } = useWindowDimensions();
    const navigation = useNavigation();

    const handleSendEmailButton = async () => {
        try {
            const response = await queries.post("/api/v1/send_email_verification", { email: email })
            if (response) {
                await storeValue("email", email)
                navigation.navigate("New password");
            }
        } catch (error) {
            console.error("Forgot password error:", error);
        }
    }

    const handleLoginButton = () => {
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
                    <CustomInput
                        placeholder="Email"
                        value={email}
                        setValue={setEmail}
                    // secureTextEntry={false}
                    />
                    <Text>We will send you a link to reset your password</Text>
                    <CustomButton
                        text="Reset password"
                        onPress={handleSendEmailButton}
                        bgColor={"black"}
                        fgColor={""}
                        icon={""}
                        type={""}
                    />
                    <CustomButton
                        text="Remember your password ? Sign in here"
                        onPress={handleLoginButton}
                        type="TERTIARY"
                        bgColor=""
                        fgColor="black"
                        icon=""
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
