import os

from junit_xml import TestCase, TestSuite


def complete_report(report, args):
    results = []

    if 'html' in args.report:
        results.append({'html_report': report.get_report(), 'title': report.title})
    if args.firstPaint > 0:
        message = ''
        if args.firstPaint < report.timing['firstPaint']:
            message = f"First paint exceeded threshold of {args.firstPaint}ms by " \
                      f"{report.timing['firstPaint'] - args.firstPaint} ms"
        results.append({"name": f"First Paint {report.title}",
                        "actual": report.timing['firstPaint'], "expected": args.firstPaint, "message": message})
    if args.speedIndex > 0:
        message = ''
        if args.speedIndex < report.timing['speedIndex']:
            message = f"Speed index exceeded threshold of {args.speedIndex}ms by " \
                      f"{report.timing['speedIndex'] - args.speedIndex} ms"
        results.append({"name": f"Speed Index {report.title}", "actual": report.timing['speedIndex'],
                        "expected": args.speedIndex, "message": message})
    if args.totalLoad > 0:
        totalLoad = report.performance_timing['loadEventEnd'] - report.performance_timing['navigationStart']
        message = ''
        if args.totalLoad < totalLoad:
            message = f"Total Load exceeded threshold of {args.totalLoad}ms by " \
                      f"{totalLoad - args.speedIndex} ms"
        results.append({"name": f"Total Load {report.title}", "actual": totalLoad,
                        "expected": args.totalLoad, "message": message})
    __process_report(results, args.report)


def __process_report(report, config):
    test_cases = []
    html_report = 0
    os.makedirs('/tmp/reports', exist_ok=True)

    for record in report:
        if 'xml' in config and 'html_report' not in record.keys():
            test_cases.append(TestCase(record['name'], record.get('class_name', 'observer'),
                                       record['actual'], '', ''))
            if record['message']:
                test_cases[-1].add_failure_info(record['message'])
        elif 'html' in config and 'html_report' in record.keys():
            with open(f'/tmp/reports/{record["title"]}_{html_report}.html', 'w') as f:
                f.write(record['html_report'])
            html_report += 1

    ts = TestSuite("Observer UI Benchmarking Test ", test_cases)
    with open("/tmp/reports/report.xml", 'w') as f:
        TestSuite.to_file(f, [ts], prettyprint=True)
