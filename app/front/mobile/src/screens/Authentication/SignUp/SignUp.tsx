import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions, Alert} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from '../../../components/CustomerButton/CustomerButton';
import SocialButton from '../../../components/SocialAuthButton/socialAuthButton';

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

import { queries } from "../../../../back-endConnection/querier";

const SignUp = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { height } = useWindowDimensions();

    const navigation = useNavigation();

    const SignInPressed =  () => {
        // if (password !== repeatPassword) {
        //     Alert.alert("Wrong password");
        //     return;
        // }
        // setIsSubmitting(true);

        // const newUser = {
        //     email: email,
        //     password: password,
        //     // email: 'test@test.com',
        //     // password: '123test',
        // };
        // try {
        //     console.log("Hello");
        //     const response = await queries.put("/register", newUser);
        //     console.log("Response", response);
        //     if (response && response.detail) {
        //         await AsyncStorage.setItem('token', response.detail);
        //         Alert.alert("Sign up sucessful");
                navigation.navigate('All');
        //     } else {
        //         setError("Try again");
        //     }
        // } catch (err) {
        //     console.error("Sign up error: ", err);
        //     setError("Error during sign up, try again");
        // } finally {
        //     setIsSubmitting(false);
        // }
    }

    const loginPressed = () => {
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgSignUpContainer}>
            <Image 
                source={AreaLogo}
                style={[styles.areaLogo, { height: height * 0.1}]}
                resizeMode="contain"
            />
                <View style={styles.SignUpContainer}>
                    <Text style={styles.SignUpTitle}>Sign Up</Text>
                    <CustomerInput
                    placeholder="Email"
                    value={email}
                    setValue={setEmail}
                    secureTextEntry={false}
                    />
                    <CustomerInput
                    placeholder="Password"
                    value={password}
                    setValue={setPassword}
                    secureTextEntry={true}
                    />
                    <CustomerInput
                    placeholder="Confirmation Password"
                    value={repeatPassword}
                    setValue={setRepeatPassword}
                    secureTextEntry={true}
                    />
                    <CustomerButton
                        text="Get started"
                        onPress={SignInPressed}
                        bgColor={"black"}
                        fgColor={""}
                    />
                    <SocialButton/>
                    <CustomerButton
                        text="Already on IFTTT ? Sign in here"
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
    bgSignUpContainer: {
        top: 20,
        marginTop: 20,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#F5F5F5',
    },
    SignUpContainer: {
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
    SignUpTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
})

export default SignUp;