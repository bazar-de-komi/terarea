import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native'

const CustomerButton = ({ onPress, text, type = "PRIMARY", bgColor, fgColor, icon}) => {
    return (
        <Pressable
        onPress={onPress}
        style={[
            styles.buttonContainer,
            styles[`buttonContainer_${type}`],
            bgColor ? {backgroundColor: bgColor} : {}
            ]}>
            
            <View style={styles.contentContainer}>
                {icon && <View style={styles.iconContainer}>{icon}</View>}
                <Text
                style={[
                    styles.text,
                    styles[`text_${type}`],
                    fgColor ? {color: fgColor} : {}
                    ]}
                >
                    {text}
                </Text>
            </View>
        </Pressable>
    )
}

//Primary for "Get started" button
//Tertiary for change page for sign in or sign up
const styles = StyleSheet.create({
    buttonContainer: {
        width: '60%',
        padding: 5,
        marginVertical: 10,
        alignItems: 'center',
        borderRadius: 20,
    },
    contentContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
    },
    iconContainer: {
        marginRight: 2,
        left: -10,
        bottom: 1,
    },
    buttonContainer_PRIMARY: {
        backgroundColor: 'black',
    },
    buttonContainer_SECONDARY: {
        borderColor: 'black',
        borderWidth: 2,
    },
    buttonContainer_TERTIARY: {
    },
    text: {
        fontWeight: 'bold',
        color: 'white'
    },
    text_TERTIARY: {
        color: 'black',
    },
    text_SECONDARY: {
        color: 'black',
    },
})

export default CustomerButton