#include <iostream>
#include <vector>
#include <chrono>
#include <ctime>
#include <ratio>

using namespace std;
using namespace std::chrono;

void selectSort(vector<int>& numbers, int begin, int end) {
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

void mergeSort(vector<int>& numbers, int begin, int end, vector<int>& temp) {
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
  temp.clear();
  int p = 0, p2 = mid;
  while(p < mid && p2 < end) {
    if(numbers[p] <= numbers[p2]) {
      temp.push_back(numbers[p]);
      p++;
    } else {
      temp.push_back(numbers[p2]);
      p2++;
    }
  }
  while(p < mid) {
    temp.push_back(numbers[p]);
    p++;
  }
  while(p2 < end) {
    temp.push_back(numbers[p2]);
    p2++;
  }
  for(int i = begin; i < end; i++) {
    numbers[i] = temp[i-begin];
  }
  temp.clear();
}

void testCase() {
}

bool checkSorted(const vector<int>& numbers) {
  for(int i = 0; i + 1 < numbers.size(); i++) {
    if(numbers[i] > numbers[i+1]) {
      return false;
    }
  }
  return true;
}

int main() {
  bool sanity_check = true;
  
  const int max_num = 200000;
  vector<int> numbers;
  for(int i = max_num - 1; i >= 0; i--) {
    numbers.push_back(i);
  }

  cout << "sorting starts." << endl;
  auto start = high_resolution_clock::now();

  vector<int> temp;
  mergeSort(numbers, 0, numbers.size(), temp);
  // selectSort(numbers, 0, numbers.size());
  
  cout << "sorting ends." << endl;
  auto stop = high_resolution_clock::now();

  auto timespan = duration_cast<microseconds>(stop - start);
  cout << "duration: " << timespan.count() / 1000000.0f << " seconds" << endl;

  if(sanity_check) {
    auto passed = checkSorted(numbers);
    if(passed) {
      cerr << "Correctly sorted." << endl;
    } else {
      cerr << "Error: numbers are not sorted." << endl;
    }
  }

  return 0;
}

