import React from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

interface Props {
  size?: 'small' | 'large';
  color?: string;
}

export default function Loading({ size = 'large', color = '#d4a84b' }: Props) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size={size} color={color} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
