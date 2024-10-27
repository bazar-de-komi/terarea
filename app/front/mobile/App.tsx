import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, SafeAreaView } from 'react-native';
import Navigation from './src/Navigation';


export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <Navigation/>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

//in root
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FBGC'
  },
});
