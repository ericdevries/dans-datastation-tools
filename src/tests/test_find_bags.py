import os

from datastation.common.find_bags import find_bags


class TestFindBags:
    def test_empty_directory_yields_empty_list(self, tmpdir):
        assert list(find_bags(tmpdir)) == []

    def test_directory_that_is_bag_yields_the_bag(self, tmpdir):
        with open(os.path.join(tmpdir, 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir)) == [tmpdir]

    def test_directory_with_bag_in_subdirectory_yields_bag(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'bag'))
        with open(os.path.join(tmpdir, 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir)) == [os.path.join(tmpdir, 'bag')]

    def test_directory_with_bag_in_subdirectory_does_not_yield_bag_when_max_depth_is_zero(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'bag'))
        with open(os.path.join(tmpdir, 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir, max_depth=0)) == []

    def test_directory_with_bag_in_subdirectory_yields_bag_when_max_depth_is_one(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'bag'))
        with open(os.path.join(tmpdir, 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir, max_depth=1)) == [os.path.join(tmpdir, 'bag')]

    def test_directory_with_bag_in_subdirectory_yields_bag_when_max_depth_is_two(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'bag'))
        with open(os.path.join(tmpdir, 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir, max_depth=2)) == [os.path.join(tmpdir, 'bag')]

    def test_default_max_depth_is_one_so_bag_in_subdirectory_will_be_found(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'bag'))
        with open(os.path.join(tmpdir, 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir)) == [os.path.join(tmpdir, 'bag')]

    def test_default_max_depth_is_one_so_bag_two_directories_down_will_not_be_found(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'subdir'))
        os.mkdir(os.path.join(tmpdir, 'subdir', 'bag'))
        with open(os.path.join(tmpdir, 'subdir', 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir)) == []

    def test_directory_with_bag_in_subdirectory_yields_bag_when_max_depth_is_negative(self, tmpdir):
        os.mkdir(os.path.join(tmpdir, 'subdir'))
        os.mkdir(os.path.join(tmpdir, 'subdir', 'subdir'))
        os.mkdir(os.path.join(tmpdir, 'subdir', 'subdir', 'subdir'))
        os.mkdir(os.path.join(tmpdir, 'subdir', 'subdir', 'subdir', 'subdir'))
        os.mkdir(os.path.join(tmpdir, 'subdir', 'subdir', 'subdir', 'subdir', 'bag'))
        with open(os.path.join(tmpdir, 'subdir', 'subdir', 'subdir', 'subdir', 'bag', 'bagit.txt'), 'w') as f:
            f.write('BagIt-Version: 1.0')
        assert list(find_bags(tmpdir, max_depth=-1)) == [
            os.path.join(tmpdir, 'subdir', 'subdir', 'subdir', 'subdir', 'bag')]
