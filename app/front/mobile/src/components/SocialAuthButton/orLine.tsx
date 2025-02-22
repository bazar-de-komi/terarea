import React from "react";
import { View, Text, StyleSheet} from 'react-native';

const OrLine = () => {
    return (
        <View style={styles.orLineContainer}>
            <View style={styles.line} />
            <Text style={styles.orLineContainer}>  Or  </Text>
            <View style={styles.line} />
        </View>
    )
}

const styles = StyleSheet.create({
    orLineContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    line: {
        flex: 1,
        height: 1,
        backgroundColor: 'black',
    },
    ortext: {
        marginHorizontal: 10,
        fontWeight: 'bold',
        color: 'black',
    },
})

export default OrLine