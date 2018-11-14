from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def process_arguments():
    latest_tag = get_latest_bacc_tag()
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--events-per-job", type=int, default=100,
                        help="Set the number of events per job")
    parser.add_argument("-n", "--n-jobs", type=int, default=10,
                        help="Set the number of jobs to submit")
    parser.add_argument("-m", "--max-jobs", type=int, default=None,
                        help="Set the maximum number of jobs to run at once")
    parser.add_argument("-o", "--out-dir", default=None,
                        help="Set the output directory")
    parser.add_argument("-s", "--bacc-setup-script", default=None,
                        help="A setup script to configure BACCARAT in each job")
    parser.add_argument("-T", "--bacc-tag", default=latest_tag,
                        help="The tag to use for BACCARAT, under CVMFS")
    parser.add_argument("-j", "--job-script-template", default=DEFAULT_TEMPLATE_JOBSCRIPT,
                        help="A template jobscript that this code fills in.")
    parser.add_argument("--job-name", default=None,
                        help="Set the job name")
    parser.add_argument("macro", help="The path to a valid BACCARAT macro to run")
    args = parser.parse_args()

    # Tweak / resolve complex args
    args.macro = os.path.realpath(args.macro)
    if not args.bacc_setup_script:
        args.bacc_setup_script = os.path.join(SETUP_BACCARAT_ON_CVMFS, args.bacc_tag, "setup.sh")
    else:
        args.bacc_setup_script = os.path.realpath(args.bacc_setup_script)
        args.bacc_tag = None
    if not os.path.isfile(args.bacc_setup_script):
        logger.error("Cannot read setup script for BACCARAT, '%s'" % args.bacc_setup_script)
        return None
    if not args.job_name:
        args.job_name = os.path.basename(os.path.splitext(args.macro)[0])

    return args
