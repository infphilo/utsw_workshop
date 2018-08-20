#include <iostream>
#include <vector>
#include <chrono>
#include <ctime>
#include <ratio>

using namespace std;
using namespace std::chrono;

void quickSort(vector<int>& numbers, int begin, int end) {
  if(end - begin <= 1)
    return;

  int pivot = end - 1;
  int pivotNumber = numbers[begin];
  for(int i = begin + 1; i < pivot; i++) {
    if(numbers[i] > pivotNumber) {
      for(; pivot > i && numbers[pivot] > pivotNumber; pivot--);
      if(pivot > i) {
	int temp = numbers[i];
	numbers[i] = numbers[pivot];
	numbers[pivot] = temp;
      }
    }
  }
  quickSort(numbers, begin, pivot);
  quickSort(numbers, pivot, end);
}

void selectSort(vector<int>& numbers) {
  for(int i = 0; i < numbers.size(); i++) {
    int minIndex = i; 
    for(int j = i + 1; j < numbers.size(); j++) {
      if(numbers[j] < numbers[minIndex]) {
	minIndex = j;
      }
    }
    int temp = numbers[i];
    numbers[i] = numbers[minIndex];
    numbers[minIndex] = temp;
  }
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
  
  const int max_num = 100000;
  vector<int> numbers;
  for(int i = max_num; i > 0; i--) {
    numbers.push_back(i);
  }

  cout << "sorting starts" << endl;
  auto start = high_resolution_clock::now();

  quickSort(numbers, 0, numbers.size());
  // selectSort(numbers);
  
  cout << "sorting ends" << endl;
  auto stop = high_resolution_clock::now();

  auto timespan = duration_cast<microseconds>(stop - start);
  cout << "duration: " << timespan.count() << " ms" << endl;

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
