#include <iostream>
#include <vector>
#include <chrono>
#include <ctime>
#include <ratio>

using namespace std;
using namespace std::chrono;

int main() {
  const int max_num = 100000000;
  vector<int> numbers;
  for(int i = max_num; i > 0; i--) {
    numbers.push_back(i);
  }

  cout << "sorting starts" << endl;
  auto start = high_resolution_clock::now();
  
  cout << "sorting ends" << endl;
  auto stop = high_resolution_clock::now();

  auto timespan = duration_cast<microseconds>(stop - start);
  cout << "duration: " << timespan.count() << "ms" << endl;

  return 0;
}
