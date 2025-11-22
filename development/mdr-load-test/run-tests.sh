#!/bin/bash

# k6 Test Runner Script
# This script provides an easy way to run different types of load tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
API_BASE_URL="${API_BASE_URL:-http://localhost:8081}"
K6_OPTIONS=""

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables from .env file if it exists
if [[ -f ".env" ]]; then
    print_info "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
fi

# Function to check if k6 is installed
check_k6() {
    if ! command -v k6 &> /dev/null; then
        print_error "k6 is not installed. Please install k6 first."
        echo "Install k6: https://grafana.com/docs/k6/latest/set-up/install-k6/"
        exit 1
    fi
    print_success "k6 is installed"
}

# Function to check if API is running
check_api() {
    print_info "Checking if API is running at $API_BASE_URL..."
    
    if curl -s -f "$API_BASE_URL/health-check" > /dev/null 2>&1; then
        print_success "API is running and accessible"
    else
        print_warning "API might not be running or accessible at $API_BASE_URL"
        print_warning "Make sure the metadata-repo-api is running before running tests"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to run a specific test
run_test() {
    local test_type=$1
    local test_file="$test_type-test.js"
    
    if [[ ! -f "$test_file" ]]; then
        print_error "Test file $test_file not found"
        exit 1
    fi
    
    print_info "Running $test_type test..."
    print_info "API Base URL: $API_BASE_URL"
    
    # Create results directory if it doesn't exist
    mkdir -p results
    
    # Generate timestamped JSON output filename if not already specified
    if [[ "$K6_OPTIONS" != *"--out json="* ]]; then
        local timestamp=$(date +"%Y%m%d_%H%M%S")
        local json_output="results/${test_type}_test_${timestamp}.json"
        K6_OPTIONS="$K6_OPTIONS --out json=$json_output"
        print_info "JSON results will be saved to: $json_output"
    fi
    
    # Set environment variable for the test
    export API_BASE_URL
    
    # Run the test
    if k6 run $K6_OPTIONS "$test_file"; then
        print_success "$test_type test completed successfully"
        
        # If JSON output was generated, show file location
        if [[ "$K6_OPTIONS" == *"--out json="* ]]; then
            local json_file=$(echo "$K6_OPTIONS" | grep -o 'json=[^ ]*' | cut -d'=' -f2)
            print_info "Results saved to: $json_file"
        fi
    else
        print_error "$test_type test failed"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] TEST_TYPE"
    echo ""
    echo "TEST_TYPE:"
    echo "  smoke       - Quick smoke test to verify basic functionality"
    echo "  functional  - Comprehensive functional testing of all endpoints"
    echo "  load        - Load test with normal expected traffic"
    echo "  stress      - Stress test with high load to find breaking points"
    echo "  spike       - Spike test with sudden traffic increases"
    echo "  all         - Run all tests in sequence"
    echo ""
    echo "OPTIONS:"
    echo "  -u, --url URL     Set API base URL (default: http://localhost:8081)"
    echo "  -o, --output FILE Set output file for results (default: auto-generated with timestamp)"
    echo "  -q, --quiet       Run in quiet mode"
    echo "  --no-color        Disable colored output"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "NOTE: JSON output is automatically generated with timestamps unless -o is specified"
    echo ""
    echo "Examples:"
    echo "  $0 smoke                                    # Run smoke test with auto JSON output"
    echo "  $0 -u http://api.example.com:8081 load     # Run load test against remote API"
    echo "  $0 -o custom_results.json stress          # Run stress test with custom output file"
    echo "  $0 all                                     # Run all tests with timestamped outputs"
}

# Function to run all tests
run_all_tests() {
    local tests=("smoke" "functional" "load" "stress" "spike")
    
    print_info "Running all tests in sequence..."
    
    for test in "${tests[@]}"; do
        print_info "Starting $test test..."
        run_test "$test"
        
        # Wait between tests
        if [[ "$test" != "spike" ]]; then
            print_info "Waiting 30 seconds before next test..."
            sleep 30
        fi
    done
    
    print_success "All tests completed!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            API_BASE_URL="$2"
            shift 2
            ;;
        -o|--output)
            K6_OPTIONS="$K6_OPTIONS --out json=$2"
            shift 2
            ;;
        -q|--quiet)
            K6_OPTIONS="$K6_OPTIONS --quiet"
            shift
            ;;
        --no-color)
            # Disable colors
            RED=""
            GREEN=""
            YELLOW=""
            BLUE=""
            NC=""
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        smoke|functional|load|stress|spike|all)
            TEST_TYPE="$1"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if test type was provided
if [[ -z "$TEST_TYPE" ]]; then
    print_error "No test type specified"
    show_usage
    exit 1
fi

# Main execution
print_info "k6 Test Runner for Metadata Repository API"
print_info "=========================================="

# Check prerequisites
check_k6
check_api

# Run the specified test(s)
if [[ "$TEST_TYPE" == "all" ]]; then
    run_all_tests
else
    run_test "$TEST_TYPE"
fi

print_success "Test execution completed!"