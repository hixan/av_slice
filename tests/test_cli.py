from av_slice.cli import video as cmd_video, audio as cmd_audio
from click.testing import CliRunner

def test_cmd_setup_video():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cmd_video, ['--help'])
    assert help_result.exit_code == 0, 'help call failed, check config'
    assert '--help' in help_result.output, 'help call failed, check config'


def test_cmd_setup_audio():
    runner = CliRunner()
    help_result = runner.invoke(cmd_audio, ['--help'])
    assert help_result.exit_code == 0, 'help call failed, check config'
    assert '--help' in help_result.output, 'help call failed, check config'


