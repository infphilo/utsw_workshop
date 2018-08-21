#include <iostream>
#include <vector>
#include <cassert>

using namespace std;
using namespace std::chrono;

void selectSort(int numbers[], int begin, int end) {
  assert(begin < end);
  for(int i = begin; i < end; i++) {
    int minIndex = i; 
    for(int j = i + 1; j < end; j++) {
      if(numbers[j] < numbers[minIndex]) {
	minIndex = j;
      }
    }
    int temp = numbers[i];
    numbers[i] = numbers[minIndex];
    numbers[minIndex] = temp;
  }
}

void mergeSort(int numbers[], int begin, int end, int temp[]) {
  if(end - begin <= 1)
    return;

  if(end - begin <= 6) {
    selectSort(numbers, begin, end);
    return;
  }

  int mid = (end + begin) / 2;
  mergeSort(numbers, begin, mid, temp);
  mergeSort(numbers, mid, end, temp);

  // perform merge
  int p = 0, p2 = mid, t = 0;
  while(p < mid && p2 < end) {
    if(numbers[p] <= numbers[p2]) {
      temp[t++] = numbers[p];
      p++;
    } else {
      temp[t++] = numbers[p2];
      p2++;
    }
  }
  while(p < mid) {
    temp[t++] = numbers[p];
    p++;
  }
  while(p2 < end) {
    temp[t++] = numbers[p2];
    p2++;
  }
  for(int i = begin; i < end; i++) {
    numbers[i] = temp[i-begin];
  }
}

bool isSame(int a[], int b[], int size) {
  for(int i = 0; i < size; i++) {
    if(a[i] != b[i])
      return false;
  }
  return true;
}

bool performTest(int question[], int answer[], int temp[], int size) {
  mergeSort(question, 0, size, temp);
  return isSame(question, answer, size);
}

void testCases() {
  int temp[10000];
  
  int question1[] = {1};
  int answer1[] = {1};

  assert(performTest(question1, answer1, temp, 1));

  int question2[] = {2, 1};
  int answer2[] = {1, 2};
  assert(performTest(question2, answer2, temp, 2));
}

bool checkSorted(int numbers[], int size) {
  for(int i = 0; i + 1 < size; i++) {
    if(numbers[i] > numbers[i+1]) {
      return false;
    }
  }
  return true;
}

int main() {
  const int max_num = 20000;
  int numbers[max_num];
  for(int i = 0; i < max_num; i++) {
    numbers[i] = max_num - i - 1;
  }

  cout << "sorting starts." << endl;
  auto start = high_resolution_clock::now();

  int temp[max_num];
  mergeSort(numbers, 0, max_num, temp);
  // selectSort(numbers, 0, max_num);

  // sort(numbers, numbers + max_num);
  
  cout << "sorting ends." << endl;
  auto stop = high_resolution_clock::now();

  auto timespan = duration_cast<microseconds>(stop - start);
  cout << "duration: " << timespan.count() / 1000000.0f << " seconds" << endl;

  auto passed = checkSorted(numbers, max_num);
  if(passed) {
    cerr << "Correctly sorted." << endl;
  } else {
    cerr << "Error: numbers are not sorted." << endl;
  }

  testCases();

  return 0;
}

